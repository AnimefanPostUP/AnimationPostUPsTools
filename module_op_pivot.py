def find_most_facing_axis(vector):
    normalized_vector = vector.normalized()
    max_component = max(abs(comp) for comp in normalized_vector)
    
    if normalized_vector.x == max_component:
        return mathutils.Vector((1.0, 0.0, 0.0))
    elif normalized_vector.x == -max_component:
        return mathutils.Vector((-1.0, 0.0, 0.0))
    elif normalized_vector.y == max_component:
        return mathutils.Vector((0.0, 1.0, 0.0))
    elif normalized_vector.y == -max_component:
        return mathutils.Vector((0.0, -1.0, 0.0))
    elif normalized_vector.z == max_component:
        return mathutils.Vector((0.0, 0.0, 1.0))
    else:
        return mathutils.Vector((0.0, 0.0, -1.0))

def setPivot(self, context):

    
    height=self.height
    direction=self.direction
    transformspace=self.transformspace
    
    if(not height):
        height="mm"
    
    if(not direction):
        height="zn"
    
    if(not transformspace):
        height="objectspace"
    
    Xpos=False
    Xneg=False
  
    Ypos=False
    Yneg=False
    
    Zpos=False
    Zneg=False
    
    tl=False
    tm=False 
    tr=False
    
    ml=False  
    mm=False
    mr=False
    
    bl=False  
    bm=False
    br=False

    objectspace=False
    worldspace=False
    auto=False
    
    
    if( transformspace=="objectspace" ):
        objectspace=True
            
    if( transformspace=="worldspace" ):
        worldspace=True
        
    if( transformspace=="auto" ):
        auto=True  
        
                     
    if( direction=="x" ):
        print("Direction : X")
        Xpos=True
    if( direction=="xn" ):
        print("Direction : -X")
        Xneg=True
        
    if( direction=="y" ):
        print("Direction : Y")
        Ypos=True
    if( direction=="yn" ):
        print("Direction : -Y")
        Yneg=True
                    
    if( direction=="z" ):
        print("Direction : Z")
        Zpos=True
    if( direction=="zn" ):
        print("Direction : -Z")
        Zneg=True
        
             
    if( height=="tl" ):
        print("Top Left")
        tl=True
    if( height=="tm" ):
        print("Top Mid")
        tm=True  
    if( height=="tr" ):
        print("Top Right")
        tr=True
    if( height=="ml" ):
        print("Mid Left")
        ml=True             
    if( height=="mm" ):
        print("Mid Mid")
        mm=True
    if( height=="mr" ):
        print("Mid Right")
        mr=True  
    if( height=="bl" ):
        print("Bottom Left")
        bl=True               
    if( height=="bm" ):
        print("Bottom Mid")
        bm=True
    if( height=="br" ):
        print("Bottom Right")
        br=True
    
    if not (worldspace or objectspace or auto):
        objectspace=True
        
    if not (tl or tm or tr or ml or mm or mr or bl or bm or br):
        mm=True
        
    if not(Xpos or Xneg or Ypos or Yneg or Zpos or Zneg):
        Zneg=True
           

    automatrixinit=mathutils.Euler((0, 0, 0), 'XYZ')
    
    selected_Objects=bpy.context.selected_objects
    wasInObjectmode=True
    
    #go to edit mode if not already 
    if bpy.context.mode != 'OBJECT':
        wasInObjectmode=False
        bpy.ops.object.mode_set(mode='OBJECT')
    
    setSelectionforAllObjects(selected_Objects, False)    

    if( height!="ct" ):
        #Correct Alignments before Setting Origins again
        for obj in selected_Objects:
            obj.select_set(True) 
        # Check if the object is a mesh
            if obj and obj.type == 'MESH':
                # Get the mesh data
                mesh = obj.data
                
                # Iterate over vertices and calculate the sum
                vert_sum = mathutils.Vector((0.0, 0.0, 0.0))
                for vert in mesh.vertices:
                    vert_sum += vert.co
                
                # Calculate the average
                avg_position_local  = vert_sum / len(mesh.vertices)
                
                # Set the pivot point to the average position
                bpy.context.scene.cursor.location = obj.matrix_world @ avg_position_local
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            obj.select_set(False) 
        bpy.context.view_layer.update()   
    
    
    for obj in selected_Objects:
        obj.select_set(True) 
    # Check if the object is a mesh

        if obj and obj.type == 'MESH':
            # Get the mesh data
            mesh = obj.data
            First=True                
            axies_x_Min=0
            axies_x_Max=0
            axies_y_Min=0
            axies_y_Max=0
            axies_z_Min=0
            axies_z_Max=0
            
            

                    
            if(auto and height!="ct"):
                pivot = obj.matrix_world @  mathutils.Vector((0.0, 0.0, 0.0)) #get Pivot
                
                Xpos=False
                Xneg=False
                Ypos=False
                Yneg=False
                Zpos=False
                Zneg=False
                
                if( direction=="x" ):
                    directionvector = mathutils.Vector((1.0, 0.0, 0.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))   
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
           
                if( direction=="xn" ):
                    directionvector = mathutils.Vector((-1.0, 0.0, 0.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))     
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
          
                if( direction=="y" ):
                    directionvector = mathutils.Vector((0.0, 1.0, 0.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))        
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
         
                if( direction=="yn" ):
                    directionvector = mathutils.Vector((0.0, -1.0, 0.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))        
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
         
                if( direction=="z" ):
                    directionvector = mathutils.Vector((0.0, 0.0, 1.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))        
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
      
                if( direction=="zn" ):                    
                    directionvector = mathutils.Vector((0.0, 0.0, -1.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))       
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
       
                    
                if(most_facing_axis.x > 0.5):
                    print("remap to x")
                    Xpos=True
                if(most_facing_axis.x < -0.5):
                    print("remap to -x")
                    Xneg=True
                if(most_facing_axis.y > 0.5):
                    print("remap to y")
                    Ypos=True
                if(most_facing_axis.y < -0.5):
                    print("remap to -y")
                    Yneg=True   
                if(most_facing_axis.z > 0.5):
                    print("remap to z")
                    Zpos=True
                if(most_facing_axis.z < -0.5):
                    print("remap to -z")
                    Zneg=True
                
      
                   
                print("target: "+str(most_facing_axis))
                       

            # Iterate over vertices and calculate the sum
            vert_sum = mathutils.Vector((0.0, 0.0, 0.0))
            for vert in mesh.vertices:
                
                if objectspace:
                    co = vert.co
                
                if worldspace:
                    co = obj.matrix_world @ vert.co
                    
                if auto:                    
                    co = vert.co
                

                if(First):
                    First=False
                    axies_x_Min=co.x
                    axies_x_Max=co.x
                    axies_y_Min=co.y
                    axies_y_Max=co.y
                    axies_z_Min=co.z
                    axies_z_Max=co.z
                    vert_sum += co
                else:
                    #override if lower or higher      
                    if co.x < axies_x_Min:
                        axies_x_Min = co.x
                    if co.x > axies_x_Max:
                        axies_x_Max = co.x
                        
                    if co.y < axies_y_Min:
                        axies_y_Min = co.y
                    if co.y > axies_y_Max:
                        axies_y_Max = co.y
                        
                    if co.z < axies_z_Min:
                        axies_z_Min = co.z
                    if co.z > axies_z_Max:
                        axies_z_Max = co.z
                        
                    vert_sum += co
                                
                                            
            # Calculate the average
            if( height=="ct" ):
                position_local  = vert_sum / len(mesh.vertices)
            
                if objectspace:
                    # Set the pivot point to the average position
                    bpy.context.scene.cursor.location = obj.matrix_world @ position_local
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                if worldspace:
                    bpy.context.scene.cursor.location = position_local
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                if auto:
                    bpy.context.scene.cursor.location = position_local
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            
            else:
                position_local = mathutils.Vector((0.0, 0.0, 0.0))
                
                # Erase Axies to set the Direction
                if( Xpos ):
                    position_local.x=axies_x_Max
                if( Xneg ):
                    position_local.x=axies_x_Min
                    
                if( Ypos ):
                    position_local.y=axies_y_Max
                if( Yneg ):
                    position_local.y=axies_y_Min
                                
                if( Zpos ):
                    position_local.z=axies_z_Max
                if( Zneg ):
                    position_local.z=axies_z_Min
                    
                #Write Axies that are used to calculate    
                
                if(Xpos or Xneg or Ypos or Yneg):
                     #Set Height
                    if(tl or tm or tr):
                       position_local.z=axies_z_Max 
                       
                    if(ml or mm or mr):
                        position_local.z=(axies_z_Min+ axies_z_Max)/2
                        
                    if(bl or bm or br):
                        position_local.z=axies_z_Min
                    
                if(Xpos or Xneg ):
                                                          
                    #Set Axies
                    if(tl or ml or tl):
                       position_local.y=axies_y_Max 
                       
                    if(tm or mm or bm):
                        position_local.y=(axies_y_Min+ axies_y_Max)/2
                        
                    if(tr or mr or br):
                        position_local.y=axies_y_Min
                        
                if(Ypos or Yneg):                  
                        
                    #Set Axies
                    if(tl or ml or tl):
                       position_local.x=axies_x_Max 
                       
                    if(tm or mm or bm):
                        position_local.x=(axies_x_Min+ axies_x_Max)/2
                        
                    if(tr or mr or br):
                        position_local.x=axies_x_Min
                        
                        
                    
                if(Zpos or Zneg):
                    
                    if(tl or tm or tr):
                       position_local.y=axies_y_Max 
                       
                    if(ml or mm or mr):
                        position_local.y=(axies_y_Min+ axies_y_Max)/2
                        
                    if(bl or bm or br):
                        position_local.y=axies_y_Min
                        
                    #Set Axies
                    if(tl or ml or bl):
                       position_local.x=axies_x_Max 
                       
                    if(tm or mm or bm):
                        position_local.x=(axies_x_Min+ axies_x_Max)/2
                        
                    if(tr or mr or br):
                        position_local.x=axies_x_Min
                        
                        
                print(str(position_local))       
                 
                if(auto):
                    bpy.context.scene.cursor.location = obj.matrix_world @ position_local
                    #bpy.context.scene.cursor.location = automatrixfixer.inverted() @ position_local #Remove the Correctionangle from Curser to align it with the Actual Object
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                if objectspace:
                    # Set the pivot point to the average position
                    bpy.context.scene.cursor.location = obj.matrix_world @ position_local
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                if worldspace:
                    bpy.context.scene.cursor.location = position_local
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                    
                
        obj.select_set(False)         
        
    setSelectionforAllObjects(selected_Objects, True)        
    
    if wasInObjectmode  :
        bpy.ops.object.mode_set(mode='OBJECT')
    else :
        bpy.ops.object.mode_set(mode='EDIT')
 
    return None