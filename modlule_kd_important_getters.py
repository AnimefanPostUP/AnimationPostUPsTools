
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

def get_current_tooldata_renamer(context):
    return bpy.context.scene.bonery_tools_data_renamer
