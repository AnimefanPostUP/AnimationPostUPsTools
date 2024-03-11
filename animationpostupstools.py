import bpy
import os
import bmesh
import math
from random import uniform
from . import bl_info
from enum import Enum
from bpy.types import Menu
import mathutils
from mathutils import Vector
import numpy as np

#List Of Keydata
class Bonery_UL_keydata(bpy.types.UIList):
    """UIList for displaying Keydata by object name"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Check if the item is valid
        if item:
            # Display the object name
            layout.label(text=item.object_name)
            # Display the vertex count
            layout.label(text=f"Groups: {len(item.vertex_group_data)}")

        else:
            layout.label(text="Invalid Keydata")
            
#List of VertexgroupData inside the selected Keydata  
class Bonery_UL_vertexgroupdata(bpy.types.UIList):
    """UIList for displaying VertexgroupData"""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Check if the item is valid
        if item:
            # Display the vertex group ID
            layout.label(text=f"ID: {item.vertex_group_id}")
            
            # Display the name of the group
            layout.label(text=f"Name: {item.vertex_group_name}")
            
        else:
            layout.label(text="Invalid VertexgroupData")

#Panel of the Bonerytool
class Bonery_PT_CorePanel(bpy.types.Panel):
    """Core Panel for Bonery addon"""
    bl_label = "Core"
    bl_idname = "BONERY_PT_core_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bonery'

    def draw(self, context):
        layout = self.layout
        scene = context.scene  
        
 

        keydata = get_current_keydata(context)
        vertexgroupdata = get_current_vertexgroupdata(context)
        
        settingsdata = get_current_settingsdata(context)
        
        if keydata is not None:
            
            row = layout.row()
            
            row = layout.row()
            row.label(text="Keys:")
            row = layout.row()
            row.template_list("Bonery_UL_keydata", "", scene.bonery_tools_data, "key_data", scene.bonery_tools_data, "active_keydata")
        
            
            row.label(text="Data")
            row = layout.row()
            row.template_list("Bonery_UL_vertexgroupdata", "", keydata, "vertex_group_data", keydata, "active_vertexgroupdata")
            
           
        row = layout.row()    
        # row.operator(Bonery_OT_keymesh.bl_idname, text="Key")
        row.operator(Bonery_OT_keyparent.bl_idname, text="Parent")
        row.operator(Bonery_OT_keyloose.bl_idname, text="Key")
        
        row = layout.row()
        row.prop(settingsdata, "flicktimeline")
        
        row = layout.row()
        row.operator(Bonery_OT_printcoordinates.bl_idname, text="Print Coordinates")

class Bonery_OT_printcoordinates(bpy.types.Operator):
    """Operator to print the vertex positions of the selected object"""
    bl_idname = "bonery.print_coordinates"
    bl_label = "Print Vertex Coordinates"
    
    def execute(self, context):
        # Get the selected object
        obj = context.object
        
        # Check if the selected object is a mesh
        if obj and obj.type == 'MESH':
            # Get the mesh data
            mesh = obj.data
            
            # Iterate over all vertices and print their positions
            for vertex in mesh.vertices:
                print(f"Vertex {vertex.index}: {vertex.co}")
        
        return {'FINISHED'}


#Change Detection    
def detect_vertexchanges_of_group( keydata_previous, keydata_current, group_name):
    """Find all vertices inside the group that have changed and return their indices and old, new positions"""
    changed_vertices = {
        "vertex_indices": [],
        "old_positions": [],
        "new_positions": []
        }
    epsilon = 1e-6  # Define a small threshold
    
    if keydata_previous and keydata_current:
        previous_group = None
        current_group = None
        for group in keydata_previous.vertex_group_data:
            if group.vertex_group_name == group_name:
                previous_group = group
                break
        for group in keydata_current.vertex_group_data:
            print("Comparing Group: "+ group.vertex_group_name)
            if group.vertex_group_name == group_name:
                current_group = group
                break
        if previous_group and current_group:
            previous_vertices = {v.vertex_id: Vector(v.vertex_position) for v in previous_group.vertex_position_data}
            current_vertices = {v.vertex_id: Vector(v.vertex_position)for v in current_group.vertex_position_data}
            for vertex_id in current_vertices:
                if vertex_id in previous_vertices:
                    diff = current_vertices[vertex_id] - previous_vertices[vertex_id]
                    if not all(abs(d) < epsilon for d in diff):
                        print("Detected Changes: "+str(len (changed_vertices)))
                        changed_vertices["vertex_indices"].append(vertex_id)
                        changed_vertices["old_positions"].append(previous_vertices[vertex_id])
                        changed_vertices["new_positions"].append(current_vertices[vertex_id])
    return changed_vertices



#Important Getters
def get_current_keydata(context):
    """Get the current active keydata"""
    tool_data = context.scene.bonery_tools_data
    if tool_data.active_keydata < len(tool_data.key_data):
        return tool_data.key_data[tool_data.active_keydata]
    return None

def get_current_vertexgroupdata(context):
    """Get the current active vertexgroupdata"""
    tool_data = context.scene.bonery_tools_data
    if tool_data.active_keydata < len(tool_data.key_data):
        key_data = tool_data.key_data[tool_data.active_keydata]
        if key_data.active_vertexgroupdata < len(key_data.vertex_group_data):
            return key_data.vertex_group_data[key_data.active_vertexgroupdata]
    return None

def get_current_settingsdata(context):
    return bpy.context.scene.bonery_settings_data


#check if keydata to object exists and if return the index in the list
def get_keydata_index_by_object_name(context, object_name):
    """Get the index of the keydata with the given object name"""
    tool_data = context.scene.bonery_tools_data
    for index, key_data in enumerate(tool_data.key_data):
        if key_data.object_name == object_name:
            return index
    return -1

def create_Keydata_by_object(context, obj):
    """Create a new keydata for the given object"""
    tool_data = context.scene.bonery_tools_data 
    key_data = tool_data.key_data.add()
    key_data.object_name = obj.name
    key_data.object_id = obj.name

    # Set index
    tool_data.active_keydata = len(tool_data.key_data) - 1
    
    # Add a group with the name "root_base"
    create_vertex_group(obj, "root_base")
    
    return key_data

#Create 
    
def create_for_vertexgroupdata(keydata, group_name):
    """Create a new vertexgroupdata for the given object"""
    # Check if the vertexgroupdata already exists
    for vertex_group_data in keydata.vertex_group_data:
        if vertex_group_data.vertex_group_name == group_name:
            return vertex_group_data
    
    # If the vertexgroupdata doesn't exist, create a new one
    vertex_group_data = keydata.vertex_group_data.add()
    vertex_group_data.vertex_group_name = group_name
    vertex_group_data.last_frame = bpy.context.scene.frame_current  # Set the last frame to the current frame of the timeline
    return vertex_group_data

def create_vertexpositiondata(vertex_group_data, vertex_id, vertex_position):
    """Create a new vertexpositiondata for the given object"""
    vertex_position_data = vertex_group_data.vertex_position_data.add()
    vertex_position_data.vertex_id = vertex_id
    vertex_position_data.vertex_position = vertex_position
    return vertex_position_data

#Getters

def get_vertexgroupdata_by_name(keydata, group_name):
    """Get the vertexgroupdata with the given name"""
    for vertex_group_data in keydata.vertex_group_data:
        if vertex_group_data.vertex_group_name == group_name:
            return vertex_group_data
    return None

def get_vertexpositiondata_by_id(vertex_group_data, vertex_id):
    """Get the vertexpositiondata with the given ID"""
    for vertex_position_data in vertex_group_data.vertex_position_data:
        if vertex_position_data.vertex_id == vertex_id:
            return vertex_position_data
    return None

#Keydata management

def remove_keydata(keydata, context):
    """Remove the given keydata from the list"""
    tool_data = context.scene.bonery_tools_data
    index = -1
    for i, kd in enumerate(tool_data.key_data):
        if kd == keydata:
            index = i
            break
    if index >= 0:
        tool_data.key_data.remove(index)
        # Set the selection index to the previous keydata if available
        if tool_data.active_keydata >= len(tool_data.key_data):
            tool_data.active_keydata = len(tool_data.key_data) - 1

def writeKeydata(keydata):
    """Write the keydata to the object"""
    obj = bpy.data.objects[keydata.object_name]
    
    # Clear existing vertex group data
    keydata.vertex_group_data.clear()
    
    groupcreated = False
    

        
    # Iterate over all vertices
    for vertex in obj.data.vertices:
        vertex_index = vertex.index

        if groupcreated: 
            obj.vertex_groups["root_base"].add([vertex_index], 1.0, 'REPLACE')
        
        # Iterate over all vertex groups
        if len (vertex.groups) <= 0 and not groupcreated:
            create_vertex_group(obj, "root_base")
            groupcreated = True
        
        for group in vertex.groups:
            group_index = group.group
            group_name = obj.vertex_groups[group_index].name
            
            #get vertex group data if it exists
            vertex_group_data = get_vertexgroupdata_by_name(keydata, group_name)
            
            # Create new vertex group data if it doesn't exist
            if vertex_group_data is None:
                vertex_group_data = create_for_vertexgroupdata(keydata, group_name)
            
            # Store vertex position data
            vertex_position_data =  create_vertexpositiondata(vertex_group_data, vertex_index, vertex.co)


#Autocreate Bones/Armatures (Bonefunctions need to be merged)

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

def checkIfBoneExists(armature, bone_name):
    if armature.type != 'ARMATURE':
        return None
    # Check if the bone already exists in the armature
    return bone_name in armature.data.edit_bones


#Viewport Modes

def armaturePosMode(armature, obj):
    # Check if armature is an Armature object
    if armature.type != 'ARMATURE':
        return None

    # Set the armature as the active object and switch to edit mode
    
    # Switch to pose mode to access the pose bones
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')    

def objectEditMode(obj):
    bpy.ops.object.mode_set(mode='OBJECT')            
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj     
    bpy.ops.object.mode_set(mode='EDIT')    

#Functions for

def copyAnimation(source_bone, target_bone, obj, armature):
    """Copy the keyframe animation from the source bone to the target bone"""

    if armature.type != 'ARMATURE':
        raise None

    if obj.pose:

        armaturePosMode(armature, obj)

        # Get the pose bones corresponding to the source and target bones
        source_pose_bone = obj.pose.bones.get(source_bone.name)
        target_pose_bone = obj.pose.bones.get(target_bone.name)

        # Check if the pose bones exist
        if source_pose_bone and target_pose_bone:
            # Copy the keyframe animation from the source bone to the target bone
            target_pose_bone.animation_data.action = source_pose_bone.animation_data.action

            print(f"Keyframe animation copied from {source_bone.name} to {target_bone.name}.")
        else:
            print("Source or target bone does not exist.")


#Cleanup

def clean_other_groups(obj, groupname, changed_vertices):
    for vertex_group in obj.vertex_groups:
        if vertex_group.name != groupname:
            for vertex_id in changed_vertices["vertex_indices"]:
                obj.vertex_groups[vertex_group.name].remove([vertex_id])

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

def createAnimation(obj, bone, transformation_matrix, last_frame):
    """Create 2 keyframes for the bone based on a transformation matrix"""
    current_frame = bpy.context.scene.frame_current
    
    # Get the object that the armature data belongs to
    armature_object = bpy.data.objects[bone.id_data.name]

    # Switch to pose mode to be able to animate bones
    bpy.ops.object.mode_set(mode='POSE')

    # Get the pose bone corresponding to the bone
    pose_bone = armature_object.pose.bones.get(bone.name)

    

    # Convert the numpy array to a Matrix
    #transformation_matrix = mathutils.Matrix(transformation_matrix.tolist())
    transformation_matrix_bone=apply_transformation_to_bone (obj, bone, transformation_matrix)

    # Decompose the transformation matrix
    loc, rot, sca = transformation_matrix_bone.decompose()

    # startframe=current_frame

    if(last_frame ==-1):
        startframe=current_frame
    else:
        startframe=last_frame

    # Set the pose bone's location, rotation, and scale and insert a keyframe
    pose_bone.keyframe_insert(data_path='location', frame=startframe+1)
    pose_bone.keyframe_insert(data_path='rotation_quaternion', frame=startframe+1)
    pose_bone.keyframe_insert(data_path='scale', frame=startframe+1)

    # Create the second keyframe 15 frames later
    bpy.context.scene.frame_set(current_frame + 15)
    pose_bone.location +=loc
    pose_bone.rotation_quaternion = pose_bone.rotation_quaternion @ rot
    #pose_bone.rotation_quaternion = rot
    pose_bone.scale *= sca
    
    
    pose_bone.keyframe_insert(data_path='location', frame=current_frame+ 15)
    pose_bone.keyframe_insert(data_path='rotation_quaternion', frame=current_frame+ 15)
    pose_bone.keyframe_insert(data_path='scale', frame=current_frame+ 15)

    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')




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
    

#Position Conversion / getter

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


def multiply_matrix(matrix, positions):
    """
    Multiply a matrix by a list of positions.
    
    Args:
        matrix (list[list[float]]): The matrix to be multiplied.
        positions (list[list[float]]): The list of positions to be multiplied.
    
    Returns:
        list[list[float]]: The resulting positions after multiplication.
    """
    result = []
    for position in positions:
        new_position = [sum(a * b for a, b in zip(row, position)) for row in matrix]
        result.append(new_position)
    return result



def returnMatrixOfAnimation_Bonespace(new_positions, obj, armature, groupbone):
    # Get the current frame
    current_frame = bpy.context.scene.frame_current
    
    # Select the armature object
    bpy.context.view_layer.objects.active = armature
    
    # Switch to pose mode to access bone transformations
    bpy.ops.object.mode_set(mode='POSE')
    
    # Get the pose bone corresponding to the groupbone
    pose_bone = armature.pose.bones.get(groupbone.name)
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
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

#Creates new Vertexgroup with Bone, tool to create subgroups of vertexgroups (used for testing)
def key_newBone(context):
    # Get the active object
    obj = bpy.context.active_object
    
    # Get the selected vertices
    selected_vertices = [v for v in obj.data.vertices if v.select]
    
    # Check if any vertices are selected
    if len(selected_vertices) == 0:
        return
    
    # Calculate the center of the selected vertices
    center = calculateCenterOfPoints([v.co for v in selected_vertices])
    
    # Create a new bone centered in the middle of the vertices
    bone_name = "new_bone"
    bone = createBoneifNotExists(obj, bone_name, center)
    
    # Get the existing vertex group name
    existing_vertex_group_name = obj.vertex_groups.active.name
    
    # Create a new vertex group with the suffix "_sub" and add the vertices
    vertex_group_name = existing_vertex_group_name + "_sub"
    create_vertex_group(obj, vertex_group_name)
    vertex_group = get_vertexgroupdata_by_name(get_current_vertexgroupdata(context), vertex_group_name)
    for vertex in selected_vertices:
        create_vertexpositiondata(vertex_group, vertex.index, vertex.co)
    
    # Parent the bone if the previous vertex group had a bone
    previous_vertex_group_name = None
    current_vertex_group_name = vertex_group_name
    vertex_groups = obj.vertex_groups
    for group in vertex_groups:
        if group.name != current_vertex_group_name:
            previous_vertex_group_name = group.name
            break
    
    if previous_vertex_group_name:
        parent_bone_name = previous_vertex_group_name
        parent_bone = getBoneifExists(obj.data, parent_bone_name)
        if parent_bone:
            copyAnimation(parent_bone, bone, obj, obj.data)
    
    # Remove the previous vertex group
    remove_vertex_groups_by_name(obj, previous_vertex_group_name)

#Creation of Vertexgroups, Armatures, Bones, Automatic tool for all in one
def key_object_loose(context):
    #get the active object
    obj = bpy.context.active_object
    alreadyExisted = False
    
    #exit editmode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #get or create keydata from object
    keydata_index = get_keydata_index_by_object_name(context, obj.name)                 
            
    if keydata_index != -1:
        alreadyExisted=True
        keydata_old = context.scene.bonery_tools_data.key_data[keydata_index]
        
        vertex_position_data_indices = [vpd.vertex_id for vpd in keydata_old.vertex_group_data[0].vertex_position_data]
        
        # Iterate over vertices that have a group contained in keydata_old but no vertex_position_data
        for vertex in obj.data.vertices:
            if not vertex.groups and vertex.index in vertex_position_data_indices:
                # Remove the vertex group from the object
                obj.vertex_groups.remove(obj.vertex_groups[keydata_old.vertex_group_data[0].vertex_group_name].index)
    
    # Add "root_base" vertex group if not exists
    if "root_base" not in obj.vertex_groups:
        obj.vertex_groups.new(name="root_base")

        
        # Iterate over vertices and apply "root_base" vertex group if not already assigned
        for vertex in obj.data.vertices:
            if not vertex.groups:
                obj.vertex_groups["root_base"].add([vertex.index], 1.0, 'REPLACE')
                
    keydata = create_Keydata_by_object(context, obj) 
    writeKeydata(keydata)

    if (alreadyExisted):
        
        # Get the selected vertices
        selected_vertices = [v for v in obj.data.vertices if v.select]

        selected_groups = []
        for vertex in selected_vertices:
            for group in vertex.groups:
                group_name = obj.vertex_groups[group.group].name
                if group_name not in selected_groups:
                    selected_groups.append(group_name)


        print(str(selected_groups))

        for selectedgroup in selected_groups:
            group=get_vertexgroupdata_by_name(keydata, selectedgroup)
            
            if(not group):
                continue
            
            #if (group.name == "root_base"):
                #continue         
            
            changed_vertices = detect_vertexchanges_of_group (keydata_old, keydata, group.vertex_group_name)
            
            if changed_vertices:
                if len(changed_vertices["vertex_indices"]) > 0:
                    
                    
                    # Iterate over vertex groups and remove "root_base" from vertices in vertex_indices
                    for vertex_group in obj.vertex_groups:
                        if vertex_group.name == "root_base":
                            for vertex_id in changed_vertices["vertex_indices"]:
                                obj.vertex_groups[vertex_group.name].remove([vertex_id])
                            break
                    
                    #Extract Data
                    vertex_indices = changed_vertices["vertex_indices"]
                    old_positions = changed_vertices["old_positions"]
                    new_positions = changed_vertices["new_positions"]
            
                    #create armature if not exists
                    armature = createArmatureifNotExists(context, obj)    
                        
                    #Pre Init Positions    
                    animatedpositions_new=new_positions
                    animatedpositions_old=old_positions
                                      
                    #If Object is already Animated this Block Fixes Transformations
                    if armature and armature.type == 'ARMATURE':
                        print("Check For: " + group.vertex_group_name)
                        bone= getBoneifExists(armature,group.vertex_group_name)
                        if bone:
                            print("Bone Exists Already, transforming Data")

                            

                            #Center locations for Animation Transformation
                            src_pivot = calculateCenterOfPoints(old_positions)
                            dst_pivot = calculateCenterOfPoints(new_positions)
                                
                            oldpos_centered = old_positions - src_pivot
                            newpos_centered = new_positions - dst_pivot

                            #Counteranimated
                            if(bone):
                                print (str(new_positions))
                                animatedpositions_new=getPositionByAnimation_Bonespace(new_positions, obj, armature, bone) 
                                animatedpositions_old=getPositionByAnimation_Bonespace(old_positions, obj, armature, bone)
                                print (str(animatedpositions_new))
                                
                                # #Overwrite Positions in Group
                                # for i, vertex_id in enumerate(changed_vertices["vertex_indices"]):
                                #     vertex_position_data = get_vertexpositiondata_by_id(group, vertex_id)
                                #     if vertex_position_data:
                                #         vertex_position_data.position = animatedpositions_new[i]
        
                        else:
                            print(f"No bone named {group.vertex_group_name} found.")

                        
                    allvertschanged = len(changed_vertices["vertex_indices"]) == len(group.vertex_position_data)          
                                                                                                 
                    transformation_matrix, src_center, dst_center= calculate_vertex_transformation(animatedpositions_old, animatedpositions_new)  
         
                    transformationM, src_c, dst_c= calculate_vertex_transformation(old_positions, new_positions)  

                        
                    # print new and old matrix
                    print("Detected Transformation:")
                    print(transformation_matrix)                         
                                            
                    objectEditMode(obj)                  
                    
                    armaturespacepos=convert_to_armature_space( armature, src_center, obj)         
                    
         
                    if(not allvertschanged):
                        print("Splitting Group, creating new Vertex Group...")
                        counter = 1
                        new_group_name = group.vertex_group_name + "_sub"
                        while new_group_name in [vg.name for vg in obj.vertex_groups]:
                            new_group_name = f"{group.vertex_group_name}_sub{counter}"
                            counter += 1
                                     
                        new_vertex_group_data = create_for_vertexgroupdata(keydata, new_group_name) 
                        bone = createBoneifNotExists(armature, group.vertex_group_name, armaturespacepos)         
                        
                        # # Apply bone animation to changed vertices
                        # for i, vertex_id in enumerate(changed_vertices["vertex_indices"]):
                        #     vertex_position_data = get_vertexpositiondata_by_id(group, vertex_id)
                        #     if vertex_position_data:
                        #         vertex_position_data.position = animatedpositions_new[i]
                        #         old_positions[i] = old_positions[i]
                        #         new_positions[i] = new_positions[i]
                        
                        # #Overwrite changed vertices in the actual Blender vertex group
                        # for i, vertex_id in enumerate(changed_vertices["vertex_indices"]):
                        #     vertex_position_data = get_vertexpositiondata_by_id(group, vertex_id)
                        #     if vertex_position_data:
                        #         vertex_position_data.position = new_positions[i]
                        #         old_positions[i] = new_positions[i]
       
                        
                    else:
                        new_vertex_group_data = group
                        
                        
                    if(not allvertschanged):
                        objectEditMode(obj)
                       
                        
                    # Remove changed vertices from the old vertex group
                    if not allvertschanged:
                        bpy.ops.object.mode_set(mode='OBJECT') 
                        old_vertex_group_data = get_vertexgroupdata_by_name(keydata, group.vertex_group_name)
                        if old_vertex_group_data:
                            for vertex_id in changed_vertices["vertex_indices"]:
                                vertex_position_data = get_vertexpositiondata_by_id(old_vertex_group_data, vertex_id)
                                if vertex_position_data:
                                    for i, vpd in enumerate(old_vertex_group_data.vertex_position_data):
                                        if vpd == vertex_position_data:
                                            print("Removed Vertex from Group")
                                            break
                                        
                        # Iterate over vertex groups and remove vertices from all other groups
                        for vertex_group in obj.vertex_groups:
                            if vertex_group.name != new_vertex_group_data.vertex_group_name:
                                for vertex_id in changed_vertices["vertex_indices"]:
                                    obj.vertex_groups[vertex_group.name].remove([vertex_id])
                        clean_other_groups(obj, new_vertex_group_data.vertex_group_name, changed_vertices["vertex_indices"])
                    
                    

                               
                    if( not allvertschanged):
                        #Add new vertex group to the object
                        create_vertex_group(obj, new_group_name)
                        
                        #set the new vertex group
                        obj.vertex_groups[new_group_name].add(changed_vertices["vertex_indices"], 1.0, 'REPLACE')
                    
                    settingsdata = get_current_settingsdata(context)
                    if(settingsdata.flicktimeline):
                        bpy.context.scene.frame_current=bpy.context.scene.frame_current+10

                    armaturePosMode(armature, obj)
                    groupbone = createBoneifNotExists(armature, new_vertex_group_data.vertex_group_name, armaturespacepos)                   
                    createAnimation(obj, groupbone, transformation_matrix, new_vertex_group_data.last_frame)
                    new_vertex_group_data.last_frame = bpy.context.scene.frame_current  # Set the last frame to the current frame of the timeline
                    objectEditMode(obj)
                    
                    #Reset the vertex positions
                    set_vertex_positions_bmesh(obj, vertex_indices, old_positions )             
                        
                    bpy.context.view_layer.update()
                    writeKeydata(keydata)
                    break
        
        remove_keydata(keydata_old, context)
        
      
    objectEditMode(obj)
    
#Calculation of the Center of the Vertex Positions
def get_vertex_Center(vertex_positions):
    """Get the center of the given vertex positions"""
    center = mathutils.Vector((0, 0, 0))
    for vertex_position in vertex_positions:
        center += vertex_position
    center /= len(vertex_positions)
    return center

#Detects Changes in Vertex Positions to detect changes in scale
def calculate_average_distance(vertex_positions, center):
    """Calculate the average distance of vertices from the center"""
    distances = [np.linalg.norm(vertex_position - center) for vertex_position in vertex_positions]
    return sum(distances) / len(distances)

#Calculation of Rotation Changes
def calculate_rotation_matrix(old_positions, new_positions, old_center, new_center):
    """Calculate the rotation matrix from old positions to new positions"""
    # Subtract centers from positions
    old_positions_centered = [pos - old_center for pos in old_positions]
    new_positions_centered = [pos - new_center for pos in new_positions]

    # Convert lists to numpy arrays
    old_positions_centered = np.array(old_positions_centered)
    new_positions_centered = np.array(new_positions_centered)

    # Calculate rotation matrix using SVD
    H = np.dot(new_positions_centered.T, old_positions_centered)
    U, S, Vt = np.linalg.svd(H)
    rotation_matrix = np.dot(Vt.T, U.T)

    return rotation_matrix

#Caculculation to find Translation
def calculateCenterOfPoints(points, axis=0):
    return  np.mean(points, axis)

#Original Function currently that is used.
def calculate_vertex_transformation(src_points, dst_points ):
       # Subtract centroids
    src_center = calculateCenterOfPoints(src_points)
    dst_center = calculateCenterOfPoints(dst_points)
    
    src_points_centered = src_points - src_center
    dst_points_centered = dst_points - dst_center

    # Compute rotation
    H = np.dot(src_points_centered.T, dst_points_centered)
    U, S, Vt = np.linalg.svd(H)
    rotation_matrix = np.dot(Vt.T, U.T)

    # Check for reflection
    if np.linalg.det(rotation_matrix) < 0:
        Vt[-1, :] *= -1
        rotation_matrix = np.dot(Vt.T, U.T)

    # Ensure smallest rotation
    d = (np.linalg.det(Vt) * np.linalg.det(U)) < 0.0
    if d:
        S[-1] = -S[-1]
        Vt[-1, :] *= -1
        rotation_matrix = np.dot(Vt.T, U.T)

    # Check for reflection
    if np.linalg.det(rotation_matrix) < 0:
        # Flip the sign of the last column of Vt
        Vt[-1, :] *= -1
        rotation_matrix = np.dot(Vt.T, U.T)
        
    #rotation_matrix = np.linalg.inv(rotation_matrix)
    
    # Compute scale
    src_points_transformed = np.dot(src_points_centered, rotation_matrix)
    scale_x = np.linalg.norm(dst_points_centered[:, 0]) / np.linalg.norm(src_points_transformed[:, 0])
    scale_y = np.linalg.norm(dst_points_centered[:, 1]) / np.linalg.norm(src_points_transformed[:, 1])
    scale_z = np.linalg.norm(dst_points_centered[:, 2]) / np.linalg.norm(src_points_transformed[:, 2])
    scale_matrix = np.diag([scale_x, scale_y, scale_z])
    
    # Debug non-matrix values
    print("Position:", dst_center - src_center)
    print("Scale:", scale_matrix)
    print("Rotation:", rotation_matrix)


    # Create transformation matrix
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = np.dot(scale_matrix, rotation_matrix)
    transformation_matrix[:3, 3] = dst_center - src_center
    
    #transformation_matrix[:3, :3] = rotation_matrix
    #transformation_matrix[:3, 3] = dst_center - rotation_matrix @ src_center
    

    return transformation_matrix, src_center, dst_center

#Combiner for the Transformation Matrix
def combine_into_transformation_matrix(translation, scale, rotation):
    """Combine translation, scale, and rotation into a transformation matrix"""
    # Create 4x4 transformation matrix
    transformation_matrix = np.eye(4)

    # Set translation
    transformation_matrix[:3, 3] = translation

    # Set scale
    transformation_matrix[:3, :3] *= scale

    # Set rotation
    transformation_matrix[:3, :3] = np.dot(transformation_matrix[:3, :3], rotation)

    return transformation_matrix





#Operators

class Bonery_OT_keymesh(bpy.types.Operator):
    """Operator for Bonery addon"""
    bl_idname = "bonery.keymesh"
    bl_label = "Key"

    def execute(self, context):      
        return {'FINISHED'}
    
class Bonery_OT_keyparent(bpy.types.Operator):
    """Operator for Bonery addon"""
    bl_idname =  "bonery.keyparent"
    bl_label = "Key"

    def execute(self, context):      
        key_newBone(context)
        return {'FINISHED'}
    
class Bonery_OT_keyloose(bpy.types.Operator):
    """Operator for Bonery addon"""
    bl_idname =  "bonery.keyloose"
    bl_label = "Key"

    def execute(self, context):      
        key_object_loose(context)
        return {'FINISHED'}
    
    
    
   
 #Data Classes  
    
class VertexPositionData(bpy.types.PropertyGroup):
    """Data for storing vertex positions"""
    vertex_position: bpy.props.FloatVectorProperty(name="Vertex Position")
    vertex_id: bpy.props.IntProperty(name="Vertex ID")

class VertexGroupData(bpy.types.PropertyGroup):
    """Data for storing vertex group IDs"""
    vertex_group_id: bpy.props.IntProperty(name="Vertex Group ID")
    vertex_group_name: bpy.props.StringProperty(name="Vertex Group ID")
    vertex_position_data: bpy.props.CollectionProperty(type=VertexPositionData, name="Vertex Position Data")
    parentId : bpy.props.IntProperty(name="Parent ID", default=-1)
    parentName : bpy.props.StringProperty(name="Parent Name", default="")
    last_frame: bpy.props.IntProperty(name="Last Frame", default=-1)

class Keydata(bpy.types.PropertyGroup):
    """Data for storing key information"""
    vertex_group_data: bpy.props.CollectionProperty(type=VertexGroupData, name="Vertex Group Data")
    object_name: bpy.props.StringProperty(name="Object Name", default="")
    object_id: bpy.props.StringProperty(name="Object ID", default="")
    active_vertexgroupdata : bpy.props.IntProperty(name="Active Index", default=0)
    
    

#Settings Data
class Settingsdata(bpy.types.PropertyGroup):
    """Settings for Bonery addon"""
    my_property: bpy.props.StringProperty(name="My Property")
    flicktimeline: bpy.props.BoolProperty(name="Flick Timeline",description="Enable or disable flicking the timeline",default=True)

class Tooldata(bpy.types.PropertyGroup):
    """Tool storage for Bonery addon"""
    my_tool: bpy.props.PointerProperty(type=bpy.types.Object, name="My Tool")
    key_data: bpy.props.CollectionProperty(type=Keydata, name="Key Data")
    active_keydata : bpy.props.IntProperty(name="Active Index", default=0)


#region <Utility> <Methods>

def register():
    """ !METHOD!
    Registrates Elements, may be used Different than usual due to the auto_load.py

    Keyword arguments:
    -
    """
    # Add property groups to scene
    #setattr(bpy.types.Scene, "uv_palettes_settings_data", bpy.props.PointerProperty(name="UV Palettes settings data", type=UVC_Data_Settings))
    setattr(bpy.types.Scene, "bonery_settings_data", bpy.props.PointerProperty(name="UV Palettes settings data", type=Settingsdata))
    setattr(bpy.types.Scene, "bonery_tools_data", bpy.props.PointerProperty(name="UV Palettes settings data", type=Tooldata))
    setattr(bpy.types.Scene, "bonery_vertex_group_data", bpy.props.PointerProperty(name="UV Palettes settings data", type=VertexGroupData))
    setattr(bpy.types.Scene, "bonery_vertex_position_data", bpy.props.PointerProperty(name="UV Palettes settings data", type=VertexPositionData))
    
    
def add_vertex_group_to_object(obj, group_name):
    """Add a vertex group to the object if it doesn't already exist"""
    if group_name not in obj.vertex_groups:
        obj.vertex_groups.new(name=group_name)
        for vertex in obj.data.vertices:
            group_index = obj.vertex_groups[group_name].index
            vertex_group = vertex.groups.get(group_index)
            if not vertex_group:
                vertex.groups.new(group_index)
                
def create_vertex_group(obj, group_name):
    """Create a vertex group with the given name on the object"""
    if group_name not in obj.vertex_groups:
        obj.vertex_groups.new(name=group_name)

#creates Vertexgroup Data
def read_vertex_groups(obj):
    """Read the vertex groups for the given object"""
    vertex_group_data = {}
    for vertex_group in obj.vertex_groups:
        group_id = int(vertex_group.name.split("_")[1])
        vertex_indices, vertex_weights = [], []
        for vertex in obj.data.vertices:
            for group in vertex.groups:
                if group.group == vertex_group.index:
                    vertex_indices.append(vertex.index)
                    vertex_weights.append(group.weight)
        position_data = VertexPositionData()
        position_data.vertex_position = vertex_group.index
        vertex_group_data[group_id] = position_data
    return vertex_group_data

#Simply Removes all Vertexgroups from an Object
def remove_vertex_groups(obj):
    """Remove all vertex groups from the given object by ID"""
    for vertex_group in obj.vertex_groups:
        obj.vertex_groups.remove(vertex_group)

#Removes a Specific Vertexgroup
def remove_vertex_groups_by_name(obj, group_name):
    """Remove vertex groups from the given object by name"""
    for vertex_group in obj.vertex_groups:
        if vertex_group.name == group_name:
            obj.vertex_groups.remove(vertex_group)

