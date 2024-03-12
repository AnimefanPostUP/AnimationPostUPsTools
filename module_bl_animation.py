
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
