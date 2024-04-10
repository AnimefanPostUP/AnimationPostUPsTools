def cleanupSharpsAndSplits(self, context):
    selected_objects = bpy.context.selected_objects
    for obj in selected_objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_sharp(clear=True)
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.merge_normals()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.shade_flat()


def smoothObjects(self, context):
    # Shade Smooth all selected Objects
    selected_Objects = bpy.context.selected_objects
    for obj in selected_Objects:
        if obj.type == 'MESH':
            # Set the object as active
            bpy.context.view_layer.objects.active = obj
            # Smooth the object
            bpy.ops.object.shade_smooth()
            # Set autosmooth value to 0
            obj.data.auto_smooth_angle = 0
    bpy.context.view_layer.update()
    
def smoothReversedSelection(self, context):
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.vertices_smooth()
    bpy.ops.mesh.select_all(action='INVERT')

def mergeNormals(self, context):
    bpy.ops.mesh.select_mode(type='EDGE')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.merge_normals()
    bpy.ops.mesh.select_all(action='DESELECT')
    
    
def splitNormals(self, context):
    settingsdata = bpy.context.scene.ttb_settings_data
    selectModeType = list(bpy.context.tool_settings.mesh_select_mode)
    autosmooth= settingsdata.autosmooth
    clear= settingsdata.cleanSplitNormals
    activeMode=False
    
    isEditMode = bpy.context.mode == 'EDIT_MESH'
  
    
    #check if self has angle attribute
    if not hasattr(self, "angle"):
        angle = settingsdata.splitangle
        activeMode = True
    else:
        angle=self.angle
        
    
        
    edgecount=0      
    selected_Objects=bpy.context.selected_objects         
    if activeMode:
        #count selected edges using bmesh
        for obj in selected_Objects:
            if not obj.type == 'MESH':
                continue
                
            #get selected edges
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            for edge in bm.edges:
                if edge.select:
                    edgecount+=1    

    #Deselect objects that arent meshes
    for obj in selected_Objects:
        if obj.type == 'MESH':
            obj.data.auto_smooth_angle = 360
        else:
            obj.select_set(False)
           
        
    if clear: # Clear if needed
        bpy.ops.mesh.customdata_custom_splitnormals_clear()    

      #go to edit mode if not already 
    if bpy.context.mode != 'EDIT_MESH':
        wasInObjectmode=True
        bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.context.tool_settings.mesh_select_mode = (False, True, False)    
        
        
    
    if clear: # Clear if needed
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_sharp(clear=True)
        mergeNormals(self, context)
   

        
           
    wasInObjectmode=False
    
    

    

        
    #Deselect all Edges first 
    bpy.ops.mesh.select_all(action='DESELECT')
    
    #Select all edges with a sharp edge angle
    bpy.ops.mesh.edges_select_sharp(sharpness=math.radians(angle))
    
    secondedgecount=0
    
    if activeMode:
        for obj in selected_Objects:
            if not obj.type == 'MESH':
                continue
                
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            for edge in bm.edges:
                if edge.select:
                    secondedgecount+=1
            
    if not activeMode:
        if edgecount>secondedgecount or edgecount<secondedgecount:
            bpy.ops.ed.undo_push(message = "Push Undo (Split Normals Operator): "+str(abs(edgecount-secondedgecount)) + " Edges Changed")
            #print(str(abs(edgecount-secondedgecount)))
    
    #Split Normals of the selected edges
    print("splitting at angle: "+ str(angle))
    bpy.ops.mesh.split_normals()
    
    if(autosmooth):
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='EDIT')
        smoothReversedSelection(self, context)
        
    #Change select mode back to original
    bpy.ops.object.mode_set(mode='EDIT')
    if selectModeType[0]:
        bpy.ops.mesh.select_mode(type='VERT')
    elif selectModeType[1]:
        bpy.ops.mesh.select_mode(type='EDGE')
    elif selectModeType[2]:
        bpy.ops.mesh.select_mode(type='FACE')
    
    if(not activeMode):
        #move back to original mode
        if (isEditMode):
            bpy.ops.object.mode_set(mode='EDIT')
        else:
            bpy.ops.object.mode_set(mode='OBJECT')     
    # if not activeMode:
    #     bpy.ops.view3d.update_edit_mesh()
            
    # if not wasInObjectmode:
    #     bpy.ops.object.mode_set(mode='OBJECT')
    # else:
    #     bpy.ops.object.mode_set(mode='EDIT')
