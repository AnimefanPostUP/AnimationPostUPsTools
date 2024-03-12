
def getAllVertexIndices(obj):
    return [vertex.index for vertex in obj.data.vertices]    

def getPositionFromIndices(obj, vertex_indices):
    return [obj.data.vertices[index].co for index in vertex_indices]

def set_vertex_positions(obj, vertex_indices, positions):
    for index, vertex_index in enumerate(vertex_indices):
        obj.data.vertices[vertex_index].co = positions[index]
        
def set_vertex_positions_bmesh(obj, vertex_indices, positions):
    # Ensure we're in object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create a bmesh from the object mesh data
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    # Ensure the vertex index table is up-to-date
    bm.verts.ensure_lookup_table()

    # Set the vertex positions
    for index, vertex_index in enumerate(vertex_indices):
        bm.verts[vertex_index].co = positions[index]

    # Update the object mesh data from the bmesh
    bm.to_mesh(obj.data)
    bm.free()

    # Update the object
    obj.data.update()
 
def set_vertex_positions_4dsafe(obj, vertex_indices, positions):
    # Iterate over the vertex indices
    for index, vertex_index in enumerate(vertex_indices):
        # Get the position
        position = positions[index]
        
        # Check if the position has 4 items
        if len(position) == 4:
            # Remove the last item
            position = position[:3]
        
        # Set the vertex position
        obj.data.vertices[vertex_index].co = position 