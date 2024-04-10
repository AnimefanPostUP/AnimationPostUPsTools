


 

def debug_write_vertex_coordinated(self, context):
        # Get the selected object
    obj = context.object
    
    # Check if the selected object is a mesh
    if obj and obj.type == 'MESH':
        # Get the mesh data
        mesh = obj.data
        
        # Iterate over all vertices and print their positions
        for vertex in mesh.vertices:
            print(f"Vertex {vertex.index}: {vertex.co}")
            
def debug_setupBone(self, context):
    # Get the selected object
    obj = context.object
    
    armature = createArmatureifNotExists(bpy.context, obj)
    centerposition = convert_to_armature_space(armature, Vector((0, 0, 0)), obj)
    groupname, group= createIncrementedVertexgroupIfNotExists(obj, "root_base")
    bone = createBoneifNotExists(armature, groupname, centerposition)
    vertex_indices = getAllVertexIndices(obj)
    applyVertexgroupToMesh(obj, groupname, vertex_indices)
    
    # Check if the selected object is a mesh
    if obj and obj.type == 'MESH':
        # Get the mesh data
        mesh = obj.data
        
        # Iterate over all vertices and print their positions
        for vertex in mesh.vertices:
            # Apply the bone's matrix to the vertex position
            transformed_position = bone.matrix @ vertex.co
            print(f"Vertex {vertex.index}: {transformed_position}")

def debug_print_vertex_withBoneAnimation(self, context):
    # Get the selected object
    obj = context.object
    if obj and obj.type == 'MESH':
        armature = createArmatureifNotExists(bpy.context, obj)
        centerposition = convert_to_armature_space(armature, Vector((0, 0, 0)), obj)
        groupname, group= createIncrementedVertexgroupIfNotExists(obj, "root_base")
        bone = createBoneifNotExists(armature, groupname, centerposition)
        vertex_indices = getAllVertexIndices(obj)
        applyVertexgroupToMesh(obj, groupname, vertex_indices)
        matrix=getMatrixOfAnimation_PoseBonespace(obj, armature, group)
        
        positions = getPositionFromIndices(obj, vertex_indices)
        
        animated_positions=multiply_matrix(matrix, positions)
        print ("Single Bone Animation: "+str(animated_positions))
        
        fullyanimated_positions=apply_transformations (obj, armature, vertex_indices, animated_positions)
        print ("Full Animation: "+str(fullyanimated_positions))
        
def debug_print_applyAnimation(self, context):
    # Get the selected object
    obj = context.object
    if obj and obj.type == 'MESH':
        armature = createArmatureifNotExists(bpy.context, obj)
        centerposition = convert_to_armature_space(armature, Vector((0, 0, 0)), obj)
        groupname, group= createIncrementedVertexgroupIfNotExists(obj, "root_base")
        bone = createBoneifNotExists(armature, groupname, centerposition)
        vertex_indices = getAllVertexIndices(obj)
        applyVertexgroupToMesh(obj, groupname, vertex_indices)
        matrix=getMatrixOfAnimation_PoseBonespace(obj, armature, group)
        
        positions = getPositionFromIndices(obj, vertex_indices)
        
        animated_positions=multiply_matrix(matrix, positions)
        print ("Single Bone Animation: "+str(animated_positions))
        
        fullyanimated_positions=apply_transformations (obj, armature, vertex_indices, animated_positions)
        print ("Full Animation: "+str(fullyanimated_positions))
        
        set_vertex_positions_4dsafe(obj, vertex_indices, fullyanimated_positions)
        removeArmatureAndVertexgroups (obj, armature)
        set_vertex_positions_4dsafe(obj, vertex_indices, fullyanimated_positions)
        
        
        