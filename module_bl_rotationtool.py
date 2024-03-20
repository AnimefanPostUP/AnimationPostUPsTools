def rotate90DegL(self, context):
    
    selected_Objects=bpy.context.selected_objects  
    setSelectionforAllObjects(selected_Objects, False)    

    for obj in selected_Objects:
        obj.select_set(True) 
        
        # Check if the object is a mesh
        if obj and obj.type == 'MESH':

            current_rotation = obj.rotation_euler
            new_rotation_z = current_rotation.z + math.radians(90)
            obj.rotation_euler = (current_rotation.x, current_rotation.y, new_rotation_z)

            mesh = obj.data           
            obj.select_set(False) 
    bpy.context.view_layer.update()   

    
    for obj in selected_Objects:
        obj.select_set(True) 
        
def rotate90DegR(self, context):
    
    selected_Objects=bpy.context.selected_objects     
    setSelectionforAllObjects(selected_Objects, False)    

    for obj in selected_Objects:
        obj.select_set(True) 
        
        # Check if the object is a mesh
        if obj and obj.type == 'MESH':

            current_rotation = obj.rotation_euler
            new_rotation_z = current_rotation.z + math.radians(-90)
            obj.rotation_euler = (current_rotation.x, current_rotation.y, new_rotation_z)
                    
            mesh = obj.data           
            obj.select_set(False) 
    bpy.context.view_layer.update()   

    
    for obj in selected_Objects:
        obj.select_set(True) 
        
        
def clipRotation(self, context):  
    selected_Objects=bpy.context.selected_objects
       
    for obj in selected_Objects:
        obj.select_set(False)
    bpy.context.view_layer.update()   

    for obj in selected_Objects:
        obj.select_set(True) 
        
    # Check if the object is a mesh
        if obj and obj.type == 'MESH':
              
            
            # Get the current rotation in radians
            current_rotation = obj.rotation_euler

            # Convert rotation to degrees
            current_rotation_degrees = [math.degrees(r) for r in current_rotation]

            # Calculate the next rotation in degrees
            next_rotation_degrees_positive = [round(angle / 15) * 15 for angle in current_rotation_degrees]
            next_rotation_degrees_negative = [(round(angle / 15) - 1) * 15 for angle in current_rotation_degrees]

            # Convert degrees back to radians
            next_rotation_radians_positive = [math.radians(angle) for angle in next_rotation_degrees_positive]
            next_rotation_radians_negative = [math.radians(angle) for angle in next_rotation_degrees_negative]

            # Calculate the difference between positive and negative rotations
            diff_positive = sum(abs(angle - current_angle) for angle, current_angle in zip(next_rotation_degrees_positive, current_rotation_degrees))
            diff_negative = sum(abs(angle - current_angle) for angle, current_angle in zip(next_rotation_degrees_negative, current_rotation_degrees))

            # Set the rotation based on the shortest path
            if diff_positive < diff_negative:
                obj.rotation_euler = next_rotation_radians_positive
            else:
                obj.rotation_euler = next_rotation_radians_negative       
            
            mesh = obj.data           
            obj.select_set(False) 
    bpy.context.view_layer.update()   

    
    for obj in selected_Objects:
        obj.select_set(True) 