                
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



  