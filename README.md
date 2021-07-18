## From Image to 3D Mode or How to create a 3D model of a photo/image for Autodesk Maya with Python

Personal project, the goal was to create 3D model from the photo/image inside Autodesk maya. 

---
### Steps to create 3D model of a photo/image.

-  Load image from the file
-  Convert image from color to grayscale
-  Take pixel intensity in grayscale which goes from 0 to 55
-  Create 3D object using the thickness of each coordinate in the picture
-  Store each vertices coordinates in the FaceLinkedList class, 
        each face (4 vertices) do have unique name (pixels coordinates X:Z)
- Save vertices coordinates in the json file
- Create poly mesh from the vertices coordinates in the json file
- Apply texture on the poly mesh
- Smooth mesh

---
### Python Module needed for this project
- opencv module
- Numpy-stl module
- Pillow module
- matplotlib module
- json module

---

![preview](https://user-images.githubusercontent.com/40180349/126080982-a966cc57-5b18-4199-94ff-cec0eb598261.png)
