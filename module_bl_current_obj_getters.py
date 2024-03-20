def get_current_Vertcount():
    """ !FUNCTION!
    Returns the Amount of Vertices in the Current Mesh
    
    :return: Amount of Vertices in the Current Mesh
    :rtype: int
    """
    functionname="GETCURRENTVERTCOUNT"
    mesh = bpy.context.object.data
    if mesh:
        return len(mesh.vertices)
    else:
        return 0