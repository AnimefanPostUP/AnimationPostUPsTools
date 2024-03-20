import bpy
import bmesh
from random import uniform
from . import bl_info
from enum import Enum
import math
import mathutils
from mathutils import Vector
from bpy.types import Menu
from bpy.types import WorkSpaceTool
import numpy as np
import os

import importlib.util
import re
import glob





# def import_functions_from_file(file_name):
#     print("running import_functions_from_file")
#     current_directory = os.path.dirname(__file__)
#     file_path = os.path.join(current_directory, file_name)
    
#     # Load the spec and module from the file path
#     spec = importlib.util.spec_from_file_location("module.name", file_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
    
#     # Use regular expression to find function definitions in the module's source
#     with open(file_path, 'r') as file:
#         content = file.read()
#     function_names = re.findall(r'def\s+(\w+)\s*\(', content)
    
#     # Get the functions from the module
#     functions = {name: getattr(module, name) for name in function_names if hasattr(module, name)}
    
#     return functions

#Function Importer
def import_function_from_file(file_name, function_name):
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, file_name)

    # Load the spec and module from the file path
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Import the function into the global namespace
    globals()[function_name] = getattr(module, function_name)


#Function Finder
def find_function_names(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
    function_names = re.findall(r'def\s+(\w+)\s*\(', content)
    return function_names

#File Finder
def find_python_files(directory):
    file_paths = glob.glob(os.path.join(directory, "*.py"))
    file_names = [os.path.basename(path) for path in file_paths]
    return file_names

#Code Injector
def inject_code_from_file(file_name):
    with open(file_name, 'r') as file:
        code = file.read()
    exec(code, globals())

# Now you can use testfunc directly
def sideloader():

    #Functionimport:
    print("SIDELOAD START")

    #get Directory
    current_directory = os.path.dirname(__file__)

    #get Python files
    files = find_python_files(current_directory)

    #fileblacklist
    fileblacklist = ["__init__.py", "auto_load.py", "animationpostupstools.py"]

    for file in files: #Iterate Files 
        if(file in fileblacklist):
            print ("SIDELOAD filter: "+file)
            continue
        print ("SIDELOAD File: "+file)
        full_file_path = os.path.join(current_directory, file)
        functionnames=find_function_names(full_file_path) #Get Functionnames
        for function_name in functionnames: #Iterate Functionnames
            print ("SIDELOAD Function: "+file+" - "+function_name)
            #import_function_from_file(full_file_path, function_name) #Import Function
            inject_code_from_file (full_file_path) #Inject Code

    print ("SIDELOAD END")

#Tester
sideloader()
sideloadtester()

#Generic Tools:
class uvc_extratoolpanel():
    """ %PANEL%
    Drawing the Colors and eventually Displayoption Buttons in Future
    """
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AnimfanPostUP"
    bl_options = {"DEFAULT_CLOSED"}
 
#Core Menu    
class extratool_PT_panel(uvc_extratoolpanel, bpy.types.Panel):
    """ %PANEL%
    Drawing the Colors and eventually Displayoption Buttons in Future
    """
    bl_idname = "anifanpostuptools_PT_extratools"
    bl_label = "Extra Tools"
     
    def draw(self, ctx):
        layout = self.layout

#Pivotsetter
class UVC_PT_extratools_1(uvc_extratoolpanel, bpy.types.Panel):
    bl_label = "Pivot Setter"
    bl_parent_id = "anifanpostuptools_PT_extratools"
    
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        settingsdata=bpy.context.scene.ttb_settings_data

        box = layout.box() #NEW BOX
        box.label(text="Set Pivot")     
        row=box.row()   
        box.label(text="Top/Bottom are Z Axies")  
        row=box.row()   
        box.label(text="in Z/Z- mode its the Y Axies")  
        
        row.prop(settingsdata, "direction", expand=True) 
        row=box.row()    
        row.prop(settingsdata, "transformspace", expand=True) 
        row=box.row()    
        
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="RADIOBUT_ON")
        op.height="tl"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="TRIA_UP")
        op.height="tm"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="RADIOBUT_ON")
        op.height="tr"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        row=box.row()    
        
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="TRIA_LEFT")
        op.height="ml"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="RADIOBUT_ON")
        op.height="mm"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="TRIA_RIGHT")
        op.height="mr"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        row=box.row()    
        
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="RADIOBUT_ON")
        op.height="bl"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="TRIA_DOWN")
        op.height="bm"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="RADIOBUT_ON")
        op.height="br"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        row=box.row()    
        
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="Average")
        op.height="ct"
        op.direction=settingsdata.direction
        op.direction=settingsdata.direction
        row=box.row()    
  
#Rotationrool        
class UVC_PT_extratools_2(uvc_extratoolpanel, bpy.types.Panel):
    bl_label = "Rotationtool"
    bl_parent_id = "anifanpostuptools_PT_extratools"
    
    
    def draw(self, context):
        layout = self.layout

        box = layout.box() #NEW BOX
        box.label(text="Rotationclip:")   
        row=box.row()   
        op=row.operator(UVC_Operator_clipRotation.bl_idname, text="Clip by 15°")
        row=box.row()   
        
        layout.row().separator()
        box.label(text="Quickrotate:")   
        row=box.row()   
        op=row.operator(UVC_Operator_rotate90DegL.bl_idname, text="Rotate L")
        row=box.row()   
        op=row.operator(UVC_Operator_rotate90DegR.bl_idname, text="Rotate R")
        row=box.row()   

#Autosmooth        
class UVC_PT_extratools_3(uvc_extratoolpanel, bpy.types.Panel):
    bl_label = "Autosmooth"
    bl_parent_id = "anifanpostuptools_PT_extratools"
    
    
    def draw(self, context):
        layout = self.layout
        box = layout.box() #NEW BOX
        row=box.row()
        
        settingsdata = bpy.context.scene.ttb_settings_data
        
        row.prop(settingsdata, "autosmooth", expand=True, text="Autosmooth")  
        row.prop(settingsdata, "cleanSplitNormals", expand=True, text="Set Clear")

        
        box.label(text="Split Normals by Degree:")   
        row=box.row()   
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="15").angle=5
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="20").angle=15
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="25").angle=25
        row=box.row()  
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="30").angle=30
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="35").angle=35
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="40").angle=40
        row=box.row()  
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="45").angle=45
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="50").angle=50
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="55").angle=55
        
        row = box.row()
        row.label(text="Active(!) Smoothing Angle:")  
        row.prop(settingsdata, "splitangle", text="" , slider=True)

class UVC_PT_extratools_4(uvc_extratoolpanel, bpy.types.Panel):
    bl_label = "Vertex Groups"
    bl_parent_id = "anifanpostuptools_PT_extratools"
    
    
    def draw(self, context):
        layout = self.layout
        box = layout.box() #NEW BOX
        row=box.row()
        
        settingsdata = bpy.context.scene.ttb_settings_data
        
        box.label(text="Select shared Vertexgroup:")   
        row=box.row()   
        op=row.operator(UVC_Operator_selectByGroup.bl_idname, text="Select SimilarGroup")

# operator UVC_Operator_selectByGroup
class UVC_Operator_selectByGroup(bpy.types.Operator):
    """ OPERATOR
    Adds a Panel
    """
    bl_idname = "anifanpostuptools.selectbygroup"
    bl_label = "Select Similar Group"
    
    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Selecting by Group")
        selectByGroup(self, ctx)
        return {'FINISHED'}
    
class UVC_Operator_selectByGroupTool(bpy.types.Operator):
    """ OPERATOR
    Adds a Panel
    """
    bl_idname = "anifanpostuptools.selectbygrouptool"
    bl_label = "Select Similar Group"
    
    def invoke(self, context, event):
        bpy.ops.ed.undo_push(message="Select By Group")
        # Perform the default selection operation
        bpy.ops.view3d.select(location=(event.mouse_region_x, event.mouse_region_y))

        # Then execute your custom operation
        selectByGroup(self, context)

        return {'FINISHED'}

class UVC_Operator_transformByGroupTool(bpy.types.Operator):
    """ OPERATOR
    Adds a Panel
    """
    bl_idname = "anifanpostuptools.transformbygrouptool"
    bl_label = "Transform Similar Group"
    
    def invoke(self, context, event):
        print("activated Transformtool")
        # Get the active mesh
        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bpy.ops.ed.undo_push(message="Select By Group Transform")
        # Initialize a list to store selected faces
        selected_faces = []

        # Iterate through faces to find selected ones
        active_face = None
        
        for face in bm.faces:
            for element in reversed(bm.select_history):
                if isinstance(element, bmesh.types.BMFace):
                    face = element
                    break

            if face is None: 
                return (None)
            if face.select and active_face is None:
                active_face=face
    
    

        if active_face is None: 
            print("canceled")
            return {'CANCELLED'}

        

        # Find the most facing axis of the active face
        most_facing_axis = find_most_facing_axis(active_face.normal)
        
        print (most_facing_axis)

        # Set the constraint axis for the transform operator
        constraint_axis = (abs(most_facing_axis.x) == 1.0, abs(most_facing_axis.y) == 1.0, abs(most_facing_axis.z) == 1.0)
        
        # Call the transform.translate operator with the constraint axis
        bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=constraint_axis)

        return {'RUNNING_MODAL'}
    
class AutoGroupSelector(WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'EDIT_MESH'

    bl_idname = "anifanpostuptools.auto_group_selector"
    bl_label = "Auto Group Selector"
    bl_description = (
        "This is a tooltip\n"
        "with multiple lines"
    )
    bl_icon = "ops.generic.select"
    bl_widget = None
    bl_operator = UVC_Operator_selectByGroupTool.bl_idname
    
    bl_keymap = (
        ("anifanpostuptools.selectbygrouptool", {"type": 'LEFTMOUSE', "value": 'PRESS'}, None),
        ("anifanpostuptools.selectbygrouptool", {"type": 'RIGHTMOUSE', "value": 'PRESS'}, None),
        ("anifanpostuptools.transformbygrouptool", {"type":"G", "value": 'PRESS'}, None),
    )

    # def draw_settings(context, layout, tool):
    #     #props = tool.operator_properties("view3d.select_lasso")
    #     #layout.prop(props, "mode")
    def draw_settings(context, layout, tool):
        pass



class UVC_Operator_setOrigin(bpy.types.Operator):

    """ OPERATOR
    Adds a Panel
    """


    bl_idname = "uvc.setorigin"
    bl_label = "sets the Origin of all Selected Objects"
    
    
    
    height: bpy.props.EnumProperty(
        items=[
            ('tl', 'Top Left', 'ltl', '', 1),
            ('tm', 'Top Mid', 'tm', '', 2),    
            ('tr', 'Top Right', 'tr', '', 3),
            ('ml', 'Mid Left', 'ml', '', 4),
            ('mm', 'Mid ', '', 'mm', 5),    
            ('mr', 'Mid Right', 'mr', '', 6),
            ('bl', 'Bottom Left', 'bl', '', 7),
            ('bm', 'Bottom Mid', 'bm', '', 8),    
            ('br', 'Bottom Right', 'br', '', 9),
            ('ct', 'Center', 'cr', '', 10),
        ],
        name="Pivot Placement",
        description="If the Pivot should be placed on a Edge, Corner or Face",
        default='mm'
    )
    

    direction: bpy.props.EnumProperty(
        items=[
            ('x', 'X', 'X', '', 1),
            ('xn', 'X-', 'X-', '', 2),    
            ('y', 'Y', 'Y', '', 3),
            ('yn', 'Y-', 'Y-', '', 4),    
            ('z', 'Z', 'Z', '', 5),
            ('zn', 'Z-', 'Z-', '', 6),    
        ],
        name="Which Direction",
        description="Which Direction to set the Pivot",
        default='zn'
    )
    
    transformspace: bpy.props.EnumProperty(
        items=[
            ('objectspace', 'Object', 'Direction by Objectspace', '', 1),
            ('worldspace', 'World', 'Direction by Worldspace', '', 2),    
            ('auto', 'Auto', 'Will Clip the Objectrotation by the most fitting Worldspace direction', '', 3),
        ],
        name="Which Direction",
        description="Which Direction to set the Pivot",
        default='objectspace'
    )
    
    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Setting Origin of Selection")
        setPivot(self=self, context=ctx)
        
        return {'FINISHED'}
    
class UVC_Operator_splitnormals(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_splitnormals"
    bl_label = "Splits the Normals of all selected Objects"
    #create integer
    angle : bpy.props.IntProperty(name="Angle", default=30, min=-360, max=360)

    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Smoothing")
        splitNormals(self=self, context=ctx)
        return {'FINISHED'}
    
    
class UVC_Operator_rotate90DegL(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_rotate90degl"
    bl_label = "Rotates 90 degrees"
    

    
    
    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Rotating")
        rotate90DegL(self=self, context=ctx)
        
        return {'FINISHED'}
  
class UVC_Operator_rotate90DegR(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_rotate90degr"
    bl_label = "Rotates 90 degrees"
    

    
    
    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Rotating")
        rotate90DegR(self=self, context=ctx)
        return {'FINISHED'}

class UVC_Operator_clipRotation(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_cliprotation"
    bl_label = "Clips the Rotation to 15 Degrees into the shortest direction"
    

    
    
    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Clipping Rotation")
        clipRotation(self=self, context=ctx)
        
        return {'FINISHED'}
    


class UVC_Operator_rerouteSnapping(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_splitnormals"
    bl_label = "Splits the Normals of all selected Objects"
    #create integer
    angle : bpy.props.IntProperty(name="Angle", default=30, min=-360, max=360)

    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Smoothing")
        splitNormals(self=self, context=ctx)
        return {'FINISHED'}

class EmptyOperator(bpy.types.Operator):
    bl_idname = "my.empty_operator"
    bl_label = "Empty Operator"

    def execute(self, context):
        return {'FINISHED'}


#Generic Tools Data:

def splitNormals_dummy(self, context):
    splitNormals(self, context)

class TTB_Data_Settings(bpy.types.PropertyGroup):
    """Stores Settings"""


    direction: bpy.props.EnumProperty(
        items=[
            ('x', 'X', 'X', '', 1),
            ('xn', 'X-', 'X-', '', 2),    
            ('y', 'Y', 'Y', '', 3),
            ('yn', 'Y-', 'Y-', '', 4),    
            ('z', 'Z', 'Z', '', 5),
            ('zn', 'Z-', 'Z-', '', 6),    
        ],
        name="Which Direction",
        description="Which Direction to set the Pivot",
        default='zn'
    )
    transformspace: bpy.props.EnumProperty(
        items=[
            ('objectspace', 'Object', 'Direction by Objectspace', '', 1),
            ('worldspace', 'World', 'Direction by Worldspace', '', 2),    
            ('auto', 'Auto', 'Will Clip the Objectrotation by the most fitting Worldspace direction', '', 3),
        ],
        name="Which Direction",
        description="Which Direction to set the Pivot",
        default='objectspace'
    )   
    cleanSplitNormals : bpy.props.BoolProperty(name="Clear Split Normals", description ="Clears Split Normals before resharpening",default= False)
    autosmooth : bpy.props.BoolProperty(name="Autosmooth", description ="Sets the Objects to Smooth Automatically",default= False)
    
    #Float Property called splitangle
    splitangle : bpy.props.FloatProperty(name="Split Angle", description ="Angle to Split Normals",default= 30, min=0, max=180, update = splitNormals_dummy)





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
class AnimationfanPostUP_PT_CorePanel(bpy.types.Panel):
    """Core Panel for Bonery addon"""
    bl_label = "Core"
    bl_idname = "anifanpostuptools_PT_core_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AnimfanPostUP'

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
        
        if(settingsdata.debuggingsubmenu):
            row = layout.box()
            row.operator(Bonery_OT_printcoordinates.bl_idname, text="Print Coordinates").operationtype=0
            row.operator(Bonery_OT_printcoordinates.bl_idname, text="Setup Bone").operationtype=1
            row.operator(Bonery_OT_printcoordinates.bl_idname, text="Print Animated Coordinates").operationtype=2
            row.operator(Bonery_OT_printcoordinates.bl_idname, text="Apply Animation").operationtype=3
            row.operator(Bonery_OT_printcoordinates.bl_idname, text="Print Coordinates").operationtype=4
            row.operator(Bonery_OT_printcoordinates.bl_idname, text="Print Coordinates").operationtype=5
            row.operator(Bonery_OT_sideloaderrecall.bl_idname, text="Sideloader Recall")


class Bonery_OT_printcoordinates(bpy.types.Operator):
    """Operator to print the vertex positions of the selected object"""
    bl_idname = "bonery.print_coordinates"
    bl_label = "Print Vertex Coordinates"
    operationtype : bpy.props.IntProperty(name="operationtype", default=0)
    
    def execute(self, context):
        if self.operationtype == 0:
            print("Operationtype 0")
            debug_write_vertex_coordinated(self, context)
            
        if self.operationtype == 1:
            print("Operationtype 1")
            debug_setupBone(self, context)
            
        if self.operationtype == 2:
            print("Operationtype 2")
            debug_print_vertex_withBoneAnimation(self, context)
            
        if self.operationtype == 3:
            print("Operationtype 3")
            debug_print_applyAnimation(self, context)
            
        if self.operationtype == 4:
            print("Operationtype 4")
            debug_write_vertex_coordinated(self, context)
        
        if self.operationtype == 5:
            print("Operationtype 4")
            testfunc()
        
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
    
class Bonery_OT_sideloaderrecall(bpy.types.Operator):
    """Operator for Bonery addon"""
    bl_idname =  "bonery.sideloader_recall"
    bl_label = "Sideloader Recall"

    def execute(self, context):      
        sideloader()
        return {'FINISHED'}    
    
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


    debuggingsubmenu: bpy.props.EnumProperty(
        items=[
            ('none', 'None', 'Hide Menus'),
            ('vertexprint', 'Vertex Print', 'Print Vertexpositions'),
            ('a', 'A', 'xxx'),
            ('b', 'B', 'xxx'),
            ('c', 'C', 'xxx'),
            ('d', 'D', 'xxx'),
            ('e', 'E', 'xxx'),
            ('f', 'F', 'xxx'),
            
        ],
        name="debugmenu",
        description="Which type of Debugging Menu to use",
        default='none'
    )
    
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
    #Generic Tools
    setattr(bpy.types.Scene, "ttb_settings_data", bpy.props.PointerProperty(name="Generic Tools settings data", type=TTB_Data_Settings))

    # tool_auto_group_selector
    # AutoGroupSelector
    
    #Register the tool using setattribute
    #setattr(bpy.types, "tool_auto_group_selector", AutoGroupSelector)
    bpy.utils.register_tool(AutoGroupSelector, after={"builtin.select_box"})

