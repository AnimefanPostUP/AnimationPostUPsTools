                
def create_vertex_group(obj, group_name):
    """Create a vertex group with the given name on the object"""
    if group_name not in obj.vertex_groups:
        obj.vertex_groups.new(name=group_name)

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
            
def add_vertex_group_to_object(obj, group_name):
    """Add a vertex group to the object if it doesn't already exist"""
    if group_name not in obj.vertex_groups:
        obj.vertex_groups.new(name=group_name)
        for vertex in obj.data.vertices:
            group_index = obj.vertex_groups[group_name].index
            vertex_group = vertex.groups.get(group_index)
            if not vertex_group:
                vertex.groups.new(group_index)
                
#Vertex Group:
def createVertexgroupIfNotExists(obj, group_name):
    if group_name not in obj.vertex_groups:
        create_vertex_group(obj, group_name)
    
def createIncrementedVertexgroupIfNotExists(obj, group_name):
    if group_name not in obj.vertex_groups:
        create_vertex_group(obj, group_name)
        return group_name, obj.vertex_groups[group_name]
    else:
        create_vertex_group(obj, group_name + "_sub")
        return group_name + "_sub", obj.vertex_groups[group_name + "_sub"]
    
    
def applyVertexgroupToMesh(obj, group_name, vertex_indices):
    for vertex_index in vertex_indices:
        obj.vertex_groups[group_name].add([vertex_index], 1.0, 'REPLACE')
        

def clean_other_groups(obj, groupname, changed_vertices):
    for vertex_group in obj.vertex_groups:
        if vertex_group.name != groupname:
            for vertex_id in changed_vertices["vertex_indices"]:
                obj.vertex_groups[vertex_group.name].remove([vertex_id])



#Used by UVC_Operator_selectByGroup from generic_toolbox_operators.py

def selectByGroup(self, ctx):
    obj = bpy.context.object
    if obj.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')

    selected_groups = get_common_vertex_groups_from_selected()

    # Ensure we're in edit mode before deselecting all
    if bpy.context.object.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')

    # bpy.ops.mesh.select_all(action='DESELECT')
    for group in selected_groups:
        select_vertices_in_group(group)

def select_vertices_in_group(group):
    obj = bpy.context.object

    # Ensure we're in object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect all vertices
    for v in obj.data.vertices:
        v.select = False

    # Save vertices in the specified group
    group_verts = [v for v in obj.data.vertices for g in v.groups if obj.vertex_groups[g.group] == group]

    # Switch back to edit mode to see the selection
    bpy.ops.object.mode_set(mode='EDIT')

    # Get a BMesh from the object's mesh data
    bm = bmesh.from_edit_mesh(obj.data)

    # Deselect all vertices in bmesh
    for v in bm.verts:
        v.select = False

    # Ensure the internal index table is up to date
    bm.verts.ensure_lookup_table()

    # Select vertices in the specified group
    for v in group_verts:
        bm.verts[v.index].select = True

    # Update the mesh to reflect the selection changes
    bmesh.update_edit_mesh(obj.data)


def get_vertex_groups_from_selected():
    obj = bpy.context.object
    selected_vertex_groups = []

    if obj.type == 'MESH':
        # Ensure we're in object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Iterate over all vertices in the mesh
        for v in obj.data.vertices:
            # If the vertex is selected
            if v.select:
                # Iterate over the vertex groups this vertex belongs to
                for g in v.groups:
                    group = obj.vertex_groups[g.group]
                    if group not in selected_vertex_groups:
                        selected_vertex_groups.append(group)

    return selected_vertex_groups

def get_common_vertex_groups_from_selected():
    obj = bpy.context.object
    common_vertex_groups = None

    if obj.type == 'MESH':
        # Ensure we're in object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Iterate over all vertices in the mesh
        for v in obj.data.vertices:
            # If the vertex is selected
            if v.select:
                # Get the vertex groups this vertex belongs to
                vertex_groups = [obj.vertex_groups[g.group] for g in v.groups]

                if common_vertex_groups is None:
                    # If this is the first selected vertex, all its groups are potential common groups
                    common_vertex_groups = set(vertex_groups)
                else:
                    # Otherwise, only keep the groups that are also in the new list
                    common_vertex_groups.intersection_update(vertex_groups)

    return list(common_vertex_groups) if common_vertex_groups else []