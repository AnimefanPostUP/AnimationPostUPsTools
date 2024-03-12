
  
#Getters  
        
def checkIfBoneExists(armature, bone_name):
    if armature.type != 'ARMATURE':
        return None
    # Check if the bone already exists in the armature
    return bone_name in armature.data.edit_bones

def getBoneifExists(armature, bone_name):
    # Check if armature is an Armature object
    if armature.type != 'ARMATURE':
        return None

    # Set the armature as the active object and switch to edit mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')

    # Check if the bone already exists
    if not checkIfBoneExists(armature, bone_name):
       return None

    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    return armature.data.bones[bone_name]

#Cleanup

def removeArmatureAndVertexgroups(obj, armature):
    # Check if the armature is the parent of the object
    if obj.parent == armature:
        # Remove the parent-child relationship
        obj.parent = None
        obj.matrix_parent_inverse = armature.matrix_world.inverted()
    
    # Remove all vertex groups associated with the object
    remove_vertex_groups(obj)
    
    # Remove the armature object
    bpy.data.objects.remove(armature, do_unlink=True)

def removeArmatureifExists(context, mesh):
    # Check if an armature with the same name already exists
    armature_name = mesh.name + "_armature"
    if armature_name in bpy.data.objects:
        # Remove the armature object
        bpy.data.objects.remove(bpy.data.objects[armature_name], do_unlink=True)
        print(f"Removed armature {armature_name}.")

#Autocreate Bones/Armatures (Bonefunctions need to be merged)
def apply_transformations(obj, armature, vertex_indices, positions):
    # Create a copy of the positions list to store the transformed positions
    transformed_positions = positions.copy()
    
    # Get the armature's pose bones
    pose_bones = armature.pose.bones
    
    # Iterate over the vertex indices and positions
    for i, vertex_index in enumerate(vertex_indices):
        # Get the vertex position
        vertex_position = positions[i]
        
        # Convert the vertex position to armature space
        vertex_position_armature_space = convert_to_armature_space(armature, vertex_position, obj)
        
        # Apply the transformations for each bone affecting the vertex
        for bone in pose_bones:
            # Get the vertex group associated with the bone
            vertex_group = obj.vertex_groups.get(bone.name)
            
            # Check if the vertex group exists and the vertex is in the vertex group
            if vertex_group and vertex_index in [g.group for g in obj.data.vertices[vertex_index].groups if g.group == vertex_group.index]:
                # Get the weight of the bone affecting the vertex
                weight = next((g.weight for g in obj.data.vertices[vertex_index].groups if g.group == vertex_group.index), 0)
                
                # Apply the bone's transformation to the vertex position
                transformed_position = vertex_position_armature_space @ bone.matrix @ bone.matrix_basis.inverted()
                
                # Apply the weight to the transformed position
                transformed_position *= weight
                
                # Convert the transformed position back to object space
                transformed_position_object_space = armature.matrix_world @ transformed_position
                
                # Update the transformed position in the list
                transformed_positions[i] = transformed_position_object_space
    
    # Return the transformed positions
    return transformed_positions


#Creators

def createArmatureifNotExists(context, mesh):
    # Check if an armature with the same name already exists
    bpy.ops.object.mode_set(mode='EDIT')
    armature_name = mesh.name + "_armature"
    if armature_name in bpy.data.objects:
        print(f"Armature {armature_name} already exists.")
        bpy.ops.object.mode_set(mode='OBJECT')
        return bpy.data.objects[armature_name]

    # Create a new armature data block
    armature_data = bpy.data.armatures.new(name=armature_name)

    # Create a new object associated with the armature data
    armature_object = bpy.data.objects.new(armature_name, armature_data)

    # Link the armature object to the current collection
    context.collection.objects.link(armature_object)
    
    # Set the armature's location to the mesh's location
    armature_object.location = mesh.location

    # Set the armature as the parent of the mesh
    mesh.parent = armature_object

    # Add an Armature modifier to the mesh
    armature_modifier = mesh.modifiers.new(name="Armature", type='ARMATURE')
    armature_modifier.object = armature_object
    armature_modifier.use_vertex_groups = True
    armature_modifier.show_in_editmode = True
    armature_modifier.show_on_cage = True
    
    print(f"Created new armature {armature_object.name} and attached it to mesh {mesh.name}.")
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return armature_object

def createBoneifNotExists(armature, bone_name, position):
    # Check if armature is an Armature object
    if armature.type != 'ARMATURE':
        return None

    # Set the armature as the active object and switch to edit mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')

    # Check if the bone already exists
    if not checkIfBoneExists(armature, bone_name):
        # Create a new bone
        new_bone = armature.data.edit_bones.new(bone_name)
        # Set the bone's head and tail
        new_bone.head = position
        new_bone.tail = position + mathutils.Vector((0, 1, 0))  # Add some length to the bone in the y-direction

    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    return armature.data.bones[bone_name]


#Get Positions

#Applies the Animation to the Mesh Coordinates to have a correct Position
def getPositionByAnimation_Bonespace(new_positions, obj, armature, groupbone):
    # Get the current frame
    current_frame = bpy.context.scene.frame_current
    
    # Select the armature object
    bpy.context.view_layer.objects.active = armature
    
    # Switch to pose mode to access bone transformations
    bpy.ops.object.mode_set(mode='POSE')
    
    # Get the pose bone corresponding to the groupbone
    pose_bone = armature.pose.bones.get(groupbone.name)
    
    # Create a list to store the transformed positions
    transformed_positions = []
    
    # Get the inverse of the object's world transformation matrix
    obj_matrix_world_inv = np.linalg.inv(obj.matrix_world)
    
    # Iterate over each new position
    for position in new_positions:
        # Convert the position to a 4-element vector
        position_4d = Vector(np.append(position, 1))

        # Transform the position to the bone space
        position_bone_space = pose_bone.matrix @ position

        # # Transform the position to the object space
        # transformed_position = obj_matrix_world_inv @ position_bone_space

        # # Convert the transformed position back to a 3D vector
        # transformed_position = transformed_position[:3]
                
        transformed_positions.append(position_bone_space)         
                
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return transformed_positions

#get Matrix of Animation
def getMatrixOfAnimation_PoseBonespace(obj, armature, groupbone):
    # Get the current frame
    current_frame = bpy.context.scene.frame_current
    
    armaturePosMode(armature, obj)
    
    # Select the armature object
    bpy.context.view_layer.objects.active = armature
    
    # Switch to pose mode to access bone transformations
    bpy.ops.object.mode_set(mode='POSE')
    
    # Get the pose bone corresponding to the groupbone
    pose_bone = armature.pose.bones.get(groupbone.name)
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    objectEditMode(obj)
    
    return pose_bone.matrix

def revertPositionByAnimation(positions, obj, armature, groupbone):
    # Get the armature object
    
    armature_object = bpy.data.objects[obj.name + "_armature"]

    # Switch to pose mode
    bpy.ops.object.mode_set(mode='POSE')

    # Iterate over the bones to find the right one
    pose_bone = None
    for bone in armature_object.pose.bones:
        if bone.name == groupbone.name:
            pose_bone = bone
            break

    # Check if pose_bone is None
    if pose_bone is None:
        raise ValueError(f"No bone found with name {groupbone.name}")

    # Apply the inverted transformation matrix to remove the animation
    print("internal calculation for corrected non animated position calculation")
    transformed_positions = []
    for position in positions:
        position_vector = Vector(position)  # Convert numpy.ndarray to Vector
        transformed_position = pose_bone.matrix.inverted() @ position_vector
        transformed_positions.append(transformed_position)

    return transformed_positions

def convert_to_armature_space(armature, position, obj):
    """Convert a position from object space to armature space."""
    
    # Convert the numpy array to a Vector
    position = Vector(np.array(position).tolist())
    
    # Convert from object space to world space
    position_world = obj.matrix_world @ position

    # Convert from world space to armature space
    position_armature = armature.matrix_world.inverted() @ position_world

    return position_armature

#Not used
def getPositionByAnimation(new_positions, obj, armature, groupbone):
    # Get the current frame
    current_frame = bpy.context.scene.frame_current
    
    # Switch to pose mode to access bone transformations
    bpy.ops.object.mode_set(mode='POSE')
    
    # Get the pose bone corresponding to the groupbone
    pose_bone = armature.pose.bones.get(groupbone)
    
    # Create a list to store the transformed positions
    transformed_positions = []
    
    # Get the inverse of the object's world transformation matrix
    obj_matrix_world_inv = np.linalg.inv(obj.matrix_world)
    
    # Iterate over each new position
    for position in new_positions:
        # Set the pose bone's location to the position
        pose_bone.location = position
        
        # Update the pose bone's transformation
        bpy.context.view_layer.update()
        
        # Get the transformed position in world space
        transformed_position_world = obj.matrix_world @ pose_bone.matrix @ Vector((0, 0, 0))
        
        # Convert the transformed position to the object's local space
        transformed_position_local = obj_matrix_world_inv @ transformed_position_world
        
        # Append the transformed position to the list
        transformed_positions.append(transformed_position_local)
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return transformed_positions

def apply_transformation_to_bone(obj, bone, transformation_matrix):
    # Convert transformation matrix from object space to bone space
    
    transformation_matrix = mathutils.Matrix(transformation_matrix.tolist())
    
    
        
    if bone.parent:
        transformation_matrix_bone = bone.parent.matrix.inverted() @ transformation_matrix
    else:
        transformation_matrix_bone = obj.matrix_world.inverted() @ transformation_matrix
       

    # Decompose the transformation matrix into its components
    location, rotation, scale = transformation_matrix_bone.decompose()

    # Invert the rotation
    rotation.invert()

    # Recompose the transformation matrix
    transformation_matrix_bone = mathutils.Matrix.Translation(location) @ rotation.to_matrix().to_4x4() @ mathutils.Matrix.Scale(scale[0], 4, (1, 0, 0)) @ mathutils.Matrix.Scale(scale[1], 4, (0, 1, 0)) @ mathutils.Matrix.Scale(scale[2], 4, (0, 0, 1))
    
    return transformation_matrix_bone 


