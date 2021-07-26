import maya.OpenMaya as OpenMaya
import json

# Location where is picture saved
picture_path = 'C:\Users\Dilan\Documents\GitHub\\from_2D_to_3D_with_python_maya'
with open('C:\Users\Dilan\Documents\GitHub\\from_2D_to_3D_with_python_maya\\vertices_position.json') as json_file:
    coordinates_data = json.load(json_file)


def create_mesh(coordinates_data, faces, merge=True):
    """
    Given a list of vertices (iterables of floats) and a list of faces (iterable of integer vert indices),
    creates and returns a maya Mesh

    :param coordinates_data: dict of the face coordinates and current face vertices position
    :type coordinates_data: dict
    :param faces: list in the list of every 4 faces number ([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
    :rtype faces: list in the list
    :param merge: if we do want to merge vertices

    :return: name of the created poly mesh
    """
    cmds.select(cl=True)
    output_mesh = OpenMaya.MObject()

    num_faces = len(faces)
    num_vertices = len(coordinates_data) * 4

    # Point array of plane vertex local positions
    vertices_xyz_pos = OpenMaya.MFloatPointArray()

    # Getting each vertices X Y Z position
    for coord, vertex_pos in sorted(coordinates_data.items()):
        for each_vt in vertex_pos:
            p = OpenMaya.MFloatPoint(each_vt[0], each_vt[1] / 5, each_vt[2])
            vertices_xyz_pos.append(p)

    # Vertex connections per poly face in one array of index into point array given above
    face_connects = OpenMaya.MIntArray()
    for eachFace in faces:
        # adding each face in to the Array
        for eachCorner in eachFace:
            face_connects.append(eachCorner)

    # An array to hold the total number of vertices that each face has, one face do have 4 vertices
    face_counts = OpenMaya.MIntArray()
    for c in range(0, num_faces):
        face_counts.append(4)

    # Creating mesh object, using arrays above
    mesh_fs = OpenMaya.MFnMesh()
    mesh_fs.create(num_vertices, num_faces, vertices_xyz_pos, face_counts, face_connects, output_mesh)
    # Getting name of new mesh
    mesh_node_name = mesh_fs.name()
    cmds.sets(mesh_node_name, add='initialShadingGroup')
    cmds.select(mesh_node_name)
    mesh_fs.updateSurface()
    # This is useful because it deletes stray vertices (those not used in any faces)
    if merge is True:
        cmds.polyMergeVertex(mesh_node_name, ch=0)
    mesh_fs.updateSurface()
    return mesh_node_name


def create_shader(name, node_type="lambert"):
    """
    Creating shader

    :param name: prefix for the shader
    :type name: str
    :param node_type: maya shader name
    :type node_type: str

    :return: material and shader
    :rtype: maya nodes
    """
    material = cmds.shadingNode(node_type, name='{name}_mat'.format(name=name), asShader=True)
    sg = cmds.sets(name='{name}_SG'.format(name=name), empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr('{mat}.outColor'.format(mat=material), '{sg}.surfaceShader'.format(sg=sg))
    return material, sg


def create_file_texture(name):
    """
    Creating file texture and place2dTexture. after connecting place2dTexture to the file texture

    :param name: prefix for the file and place2dTexture node name
    :type name: str

    :return: file node name and place2dTexture node name
    :rtype: maya nodes
    """
    texture_file = cmds.shadingNode('file', name='{name}_file'.format(name=name), asTexture=True, isColorManaged=True)
    place2dTextureNode = cmds.shadingNode('place2dTexture',
                                          name='{name}_place2dTexture'.format(name=name),
                                          asUtility=True)

    cmds.connectAttr('{p2d}.outUV'.format(p2d=place2dTextureNode), '{tex}.uvCoord'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.outUvFilterSize'.format(p2d=place2dTextureNode),
                     '{tex}.uvFilterSize'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.vertexCameraOne'.format(p2d=place2dTextureNode),
                     '{tex}.vertexCameraOne'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.vertexUvOne'.format(p2d=place2dTextureNode), '{tex}.vertexUvOne'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.vertexUvThree'.format(p2d=place2dTextureNode),
                     '{tex}.vertexUvThree'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.vertexUvTwo'.format(p2d=place2dTextureNode), '{tex}.vertexUvTwo'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.coverage'.format(p2d=place2dTextureNode), '{tex}.coverage'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.mirrorU'.format(p2d=place2dTextureNode), '{tex}.mirrorU'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.mirrorV'.format(p2d=place2dTextureNode), '{tex}.mirrorV'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.noiseUV'.format(p2d=place2dTextureNode), '{tex}.noiseUV'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.offset'.format(p2d=place2dTextureNode), '{tex}.offset'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.repeatUV'.format(p2d=place2dTextureNode), '{tex}.repeatUV'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.rotateFrame'.format(p2d=place2dTextureNode), '{tex}.rotateFrame'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.rotateUV'.format(p2d=place2dTextureNode), '{tex}.rotateUV'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.stagger'.format(p2d=place2dTextureNode), '{tex}.stagger'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.translateFrame'.format(p2d=place2dTextureNode),
                     '{tex}.translateFrame'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.wrapU'.format(p2d=place2dTextureNode), '{tex}.wrapU'.format(tex=texture_file))
    cmds.connectAttr('{p2d}.wrapV'.format(p2d=place2dTextureNode), '{tex}.wrapV'.format(tex=texture_file))
    return texture_file, place2dTextureNode


faces = []
# Creating dummy list to store one face
dummy = []
n = 0
# For each 4 coordinates appending one face
# Every 4 faces storing in the own list, it needed to be able to merge vertices later when we do create poly mesh
for i in range(len(coordinates_data) * 4):
    n += 1
    dummy.append(i)
    if n == 4:
        faces.append(dummy)
        dummy = []
        n = 0

# Creating poly mesh
mesh_name = create_mesh(coordinates_data, faces)
# Making UVs for poly mesh
cmds.polyProjection('{name}.f[0:{total_faces}]'.format(name=mesh_name, total_faces=len(coordinates_data)),
                    constructionHistory=True,
                    type='Planar',
                    insertBeforeDeformers=False,
                    sf=True,
                    md='b')

# Assign shader to the mesh
mtl, sg = create_shader(mesh_name)
cmds.sets(mesh_name, edit=True, forceElement=sg)

# Connecting file texture to the shader
file_node, place2dTextureNode = create_file_texture(mesh_name)
cmds.connectAttr('{node}.outColor'.format(node=file_node), '{node}.color'.format(node=mtl))

# Sets Texture and rote texture
cmds.setAttr('{node}.fileTextureName'.format(node=file_node),
             '{path}\converted.png'.format(path=picture_path),
             type='string')
cmds.setAttr('{node}.rotateUV'.format(node=place2dTextureNode), 180)

# Smooth model once
cmds.polySmooth(mesh_name, dv=1)
cmds.select(d=True)
