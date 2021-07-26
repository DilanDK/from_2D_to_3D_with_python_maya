import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import json
"""
installed:
    opencv-python module
    Numpy-stl module
    Pillow - module
    matplotlib - module
    json - module
"""


class Node:
    """
    Data structure that keeps track of face coordinates and current face vertices position
    """
    def __init__(self, xz, coordinates, next=None):
        self.xz = xz
        self.coordinates = coordinates
        self.next = next


class FaceLinkedList:
    """
    Class writing and reading information from the Node class
    """
    def __init__(self):
        self.head = None

    def write_vertices(self, xz, coordinates):
        """
        Writing face XZ position and vertices coordinates in to the Node class. After pointing to the previous Node

        :param xz: face XZ position in maya space
        :type xz: str
        :param coordinates: Writing 4 vertices position  in maya space
        :type: coordinates: list in the list
        """
        node = Node(xz, coordinates, self.head)
        self.head = node

    def get_vertices(self, xz):
        """
        Getting current face vertices coordinates in maya space

        :param xz: face XZ coordinates in maya space
        :type xz: str
        :return: current face vertices coordinates in maya space
        :rtype: list in the list
        """
        iterator = self.head
        index = 0
        while iterator:
            if xz == iterator.xz:
                return [iterator.coordinates]
            iterator = iterator.next
            index += 1


# FaceLinkedList is used in the get_coord_from_img and in sorting dict which one will be saved in the file
fll = FaceLinkedList()


def get_coord_from_img(max_img_size, image_path, max_vertices_height):
    """
    1.  Load image from the file
    2.  Convert image from color to grayscale
    3.  Take pixel intensity in grayscale which goes from 0 to 55
    4.  Create 3D object using the thickness of each coordinate in the picture
    5.  Storing each vertices coordinates in the FaceLinkedList class,
        each face (4 vertices) do have unique name (pixels coordinates X:Z)

    :param max_img_size: image will be converted in to maximum size
    :type max_img_size: tuple
    :param image_path: image path
    :type image_path: str
    :param max_vertices_height: max vertices height which can reach on Y coordinates
    :type image_path: int

    :return: number of rows and columns
    :rtype: int
    """
    # Converting image to grayscale
    img = Image.open(image_path)
    grey_img = img.convert('L')
    rgb_img = img.convert('RGB')

    # Resizing img if needed
    grey_img.thumbnail(max_img_size)
    rgb_img.thumbnail(max_img_size)

    # Converting img to the array
    image_np = np.array(grey_img)

    # Getting Max and Min pixel Intensity
    max_pix = image_np.max()

    # nr_cols up/down, nr_rows - left/right
    (nr_cols, nr_rows) = grey_img.size

    # Logic of getting each pixel coordinates and storing each faces vertices
    for z in range(0, nr_cols):
        for x in range(0, nr_rows):
            pixel_intensity = image_np[x][z]
            # y is to height, so we making it smaller
            y = (pixel_intensity * max_vertices_height) / max_pix
            # Storing current 4 coordinates in the temp list, for easy reading and debugging
            coordinates = []
            coordinates.append([x, y, z])
            coordinates.append([x-1, y, z])
            coordinates.append([x-1, y, z + 1])
            coordinates.append([x, y, z + 1])

            # Storing coordinates of first row
            if z == 0:
                # To align two vertices with previous face (vertex number 2 and 3),
                # We get previous face two vertices position and rewriting it in the current
                if x != 0:
                    new_coordinates = [coordinates[0],
                                       fll.get_vertices('{x}:{z}'.format(x=x - 1, z=z))[0][0],
                                       fll.get_vertices('{x}:{z}'.format(x=x - 1, z=z))[0][3],
                                       coordinates[3]]
                    fll.write_vertices('{x}:{z}'.format(x=x, z=z), new_coordinates)

                # If it is the first column in the first row, we do save original vertices position
                else:
                    fll.write_vertices('{x}:{z}'.format(x=x, z=z), coordinates)

            # Storing rest coordinates of the rows
            else:
                # First column
                # To align two vertices with previous face (vertex number 1 and 2),
                # We get previous face two vertices position and rewriting it in the current
                if x == 0:
                    new_coordinates = [fll.get_vertices('{x}:{z}'.format(x=x, z=z - 1))[0][3],
                                       fll.get_vertices('{x}:{z}'.format(x=x, z=z - 1))[0][2],
                                       coordinates[2],
                                       coordinates[3]]
                    fll.write_vertices('{x}:{z}'.format(x=x, z=z), new_coordinates)

                # Rest columns
                # To align two vertices with previous face (vertex number 1, 2, 3),
                # We get previous face three vertices position and rewriting it in the current
                elif x != 0:
                    new_coordinates = [fll.get_vertices('{x}:{z}'.format(x=x, z=z - 1))[0][3],
                                       fll.get_vertices('{x}:{z}'.format(x=x - 1, z=z))[0][0],
                                       fll.get_vertices('{x}:{z}'.format(x=x - 1, z=z))[0][3],
                                       coordinates[3]]
                    fll.write_vertices('{x}:{z}'.format(x=x, z=z), new_coordinates)

    # Flipping image and saving new image,
    # This step needed for maya texture
    out = rgb_img.transpose(Image.FLIP_LEFT_RIGHT)
    out.save("converted.png", format="png")
    return nr_cols, nr_rows


# Getting number of columns, rows and storing all faces coordinates in the FaceLinkedList
nr_cols, nr_rows = get_coord_from_img((350, 350), 'city4.jpg', 280)

# Writing all faces coordinates in to the dict, key is XZ faces pivot point coordinates,
# Value is faces vertices coordinates
all_vertices = {}
for z in range(0, nr_cols):
    for x in range(0, nr_rows):
        coordinates = fll.get_vertices('{x}:{z}'.format(x=x, z=z))[0]
        all_vertices['{x}:{z}'.format(x=x, z=z)] = coordinates

# Writing all information in to the file
with open('vertices_position.json', 'w') as f:
    json.dump(all_vertices, f)

f.close()