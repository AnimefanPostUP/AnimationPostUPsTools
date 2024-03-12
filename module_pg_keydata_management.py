#check if keydata to object exists and if return the index in the list
def get_keydata_index_by_object_name(context, object_name):
    """Get the index of the keydata with the given object name"""
    tool_data = context.scene.bonery_tools_data
    for index, key_data in enumerate(tool_data.key_data):
        if key_data.object_name == object_name:
            return index
    return -1

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