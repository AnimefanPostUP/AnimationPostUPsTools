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
from mathutils import Euler
import numpy as np
import os

import importlib.util
import re
import glob


####################################################################################################
#02_menu_pivotsetter_a.pymodule
####################################################################################################


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
    
class UVC_Operator_rename(bpy.types.Operator):
    """ OPERATOR
    Adds a Panel
    """
    bl_idname = "anifanpostuptools.rename"
    bl_label = "Rename"

    PreFix: bpy.props.StringProperty(name="Prefix", default="")
    Suffix: bpy.props.StringProperty(name="Suffix", default="") 
    Suffix_Sub: bpy.props.StringProperty(name="Suffix Sub", default="")
    
    def execute(self, context):
        bpy.ops.ed.undo_push(message="Rename")
        rename (self=self, context=context)
        return {'FINISHED'}
    
def rename(self, context):
    # Get active Objects
    selected_Objects = bpy.context.selected_objects

    # Get Prefix and Suffix from Operator
    prefix = self.PreFix
    suffix = self.Suffix
    suffix_Sub = self.Suffix_Sub

    prefixIsSet = False
    suffixIsSet = False
    suffix_SubIsSet = False

    if not prefix == "":
        prefixIsSet = True

    if not suffix == "":
        suffixIsSet = True

    if not suffix_Sub == "":
        suffix_SubIsSet = True

    # Select the objects you want to rename
    selected_objects = bpy.context.selected_objects
    for obj in selected_objects:
        new_name = prefix if prefixIsSet else ""
        if suffixIsSet:
            new_name += f"_{suffix}" if prefixIsSet else suffix
        if suffix_SubIsSet:
            new_name += f"_{suffix_Sub}" if new_name else suffix_Sub
        obj.name = new_name
        
        

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

        currentOrientationMode = bpy.context.scene.transform_orientation_slots[0].type
        #Set mode to local
        bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
        
        # Set the constraint axis for the transform operator
        constraint_axis = (abs(most_facing_axis.x) == 1.0, abs(most_facing_axis.y) == 1.0, abs(most_facing_axis.z) == 1.0)
        
        # Call the transform.translate operator with the constraint axis
        bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=constraint_axis)
        
        #revert to old mode
        bpy.context.scene.transform_orientation_slots[0].type = currentOrientationMode

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


class AutoGroupSelectorObject(WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'

    bl_idname = "anifanpostuptools.auto_group_selector_object"
    bl_label = "Auto Group Selector"
    bl_description = (
        "This is a tooltip\n"
        "with multiple lines"
    )
    bl_icon = "ops.generic.select"
    bl_widget = None
    bl_operator = "view3d.select"
    
    bl_keymap = (
        ("view3d.select", {"type": 'RIGHTMOUSE', "value": 'PRESS'}, None),
        ("view3d.select", {"type": 'RIGHTMOUSE', "value": 'CLICK_DRAG'}, None),
    )

    def draw_settings(context, layout, tool):
        pass
    

    




####################################################################################################
#02_menu_pivotsetter_op.pymodule
####################################################################################################

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

####################################################################################################
#03_menu_autosmooth_a.pymodule
####################################################################################################



####################################################################################################
#03_menu_autosmooth_op.pymodule
####################################################################################################



####################################################################################################
#04_menu_rotationtool_a.pymodule
####################################################################################################

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
        op=row.operator(UVC_Operator_rotate90DegL.bl_idname, text="Rotate L.")
        row=box.row()   
        op=row.operator(UVC_Operator_rotate90DegR.bl_idname, text="Rotate R.")
        row=box.row()   
        
        #Create Operator to fix the rotation of the object by selected face normal
        #create one operator that allows to fix x,y,z, or all axis
        
        #Operator
        row=box.row()
        row.label(text="Fix Rotation by Face Normal:")
        row=box.row()
        op=row.operator(UVC_Operator_fixRotation.bl_idname, text="X Axis")
        op.axis = 'X'
        op.reset = False
        op=row.operator(UVC_Operator_fixRotation.bl_idname, text="Y Axis")
        op.axis = 'Y'
        op.reset = False
        op=row.operator(UVC_Operator_fixRotation.bl_idname, text="Z Axis")
        op.axis = 'Z'
        op.reset = False
        op=row.operator(UVC_Operator_fixRotation.bl_idname, text="All Axis")
        op.axis = 'A'
        op.reset = False
        
        #Operator
        row.label(text="Fix Rotation and Apply:")
        row=box.row()
        op=row.operator(UVC_Operator_fixRotation.bl_idname, text="X Fix")
        op.axis = 'X'
        op.reset = True
        op=row.operator(UVC_Operator_fixRotation.bl_idname, text="Y Fix")
        op.axis = 'Y'
        op.reset = True   
        op=row.operator(UVC_Operator_fixRotation.bl_idname, text="Z Fix")
        op.axis = 'Z'
        op.reset = True
        op=row.operator(UVC_Operator_fixRotation.bl_idname, text="All Fix")
        op.axis = 'A'
        op.reset = True

####################################################################################################
#04_menu_rotationtool_op.pymodule
####################################################################################################

#Operator
class UVC_Operator_fixRotation(bpy.types.Operator):
    """ OPERATOR
    Adds a Panel
    """
    bl_idname = "anifanpostuptools.fixrotation"
    bl_label = "Fix Rotation"
    
    #create enums
    axis: bpy.props.EnumProperty(
        items=[
            ('X', "X Axis", ""),
            ('Y', "Y Axis", ""),
            ('Z', "Z Axis", ""),
            ('A', "All Axis", ""),
        ],
        name="Axis",
        description="Select the Axis to fix",
        default='A'
    )
    
    #boolean called "reset"
    reset: bpy.props.BoolProperty(
        name="Reset",
        description="Reset the Rotation",
        default=False
    )
    
    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Fixing Rotation")
        fixRotation(self=self, ctx=ctx)
        return {'FINISHED'}
    
    

def fixRotation(self, ctx):
    #get selected object and make sure in edit mode
    obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')
    
    #get the selected using bmesh
    bm = bmesh.from_edit_mesh(obj.data)
    selected = [f for f in bm.faces if f.select]
    
    #rotate the object by the selected face normal so the normal is in the direction of the axis of the world
    for face in selected:
        normal = face.normal
        if self.axis == 'X':
            target = Vector((1, 0, 0))
        elif self.axis == 'Y':
            target = Vector((0, 1, 0))
        elif self.axis == 'Z':
            target = Vector((0, 0, 1))
        elif self.axis == 'A':
            target = Vector((1, 1, 1))
        
        rotation = normal.rotation_difference(target)
        
        # Apply the rotation to the entire object
        obj.rotation_euler = rotation.to_euler()
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #save the rotations before applying the rotation
    oldrotation = obj.rotation_euler.copy()
    
    if self.reset:
        if self.reset==True:
            #apply the rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            #reapply the old rotation  inverted 
            
            #make the euler -x -y -z
            newrotation = Euler((-oldrotation.x, -oldrotation.y, -oldrotation.z))
            obj.rotation_euler = newrotation
            
        
    
    
    
        
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

####################################################################################################
#05_menu_autosmooth_a.pymodule
####################################################################################################

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

        row.prop(settingsdata, "extendsplitnormalmenu", expand=True, text="Expand")
        
        
        box.label(text="Split Normals by Degree:")   

        #===
        row=box.row()   
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="5").angle=5
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="8").angle=7

        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="10").angle=10
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="13").angle=13
        
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="15").angle=15
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="15").angle=18
       
        #===
        row=box.row() 
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="20").angle=20
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="23").angle=23

        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="25").angle=25
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="28").angle=28

        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="30").angle=30
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="33").angle=33
        
        #===
        row=box.row()  
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="35").angle=35
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="38").angle=38

        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="40").angle=40
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="43").angle=43

        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="45").angle=45
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="48").angle=48

        #===
        row=box.row()  
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="50").angle=50
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="53").angle=53

        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="55").angle=55
        if(settingsdata.extendsplitnormalmenu):
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="58").angle=58

        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="60").angle=60




        if(settingsdata.extendsplitnormalmenu):
            #===
            row=box.row()  
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="65").angle=65
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="70").angle=70
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="75").angle=75
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="80").angle=80
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="85").angle=85

            row=box.row()  
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="90").angle=90
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="95").angle=95
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="100").angle=100
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="105").angle=105
            op=row.operator(UVC_Operator_splitnormals.bl_idname, text="110").angle=110

        
        row = box.row()
        row.label(text="Clean Sharps/Splits/Shade:")  
        op=row.operator(UVC_Operator_cleanupsharps.bl_idname, text="Clean")

        row = box.row()
        row.label(text="Active(!) Smoothing Angle:")  
        row.prop(settingsdata, "splitangle", text="" , slider=True)


####################################################################################################
#05_menu_autosmooth_b.pymodule
####################################################################################################

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
    
class UVC_Operator_cleanupsharps(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_cleanupsharps"
    bl_label = "Cleans, Sharps, Splits and Shading"

    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Cleanup Sharps")
        cleanupSharpsAndSplits(self=self, context=ctx)
        return {'FINISHED'}
    


####################################################################################################
#06_menu_renamer_a.pymodule
####################################################################################################

class UVC_PT_extratools_5(uvc_extratoolpanel, bpy.types.Panel):
    bl_label = "Renamer"
    bl_parent_id = "anifanpostuptools_PT_extratools"
    
    
    def draw(self, context):
        layout = self.layout
        box = layout.box() #NEW BOX
        row=box.row()

        Tooldata_Renamer= get_current_tooldata_renamer(context) #Get Tooldata



        #Prop Prefix
        row=box.row()
        row.prop (Tooldata_Renamer, "Prefix", text="Prefix")
        row=box.row()
        row.label(text="_")
        row=box.row()
        row.prop (Tooldata_Renamer, "Suffix", text="Suffix")




        box = layout.box() #NEW BOX
        row=box.row()
        row.label(text="Size:", icon="CON_SIZELIMIT")

        row=box.row()
        subsuffix="none"
        op=row.operator(UVC_Operator_rename.bl_idname, text="None")
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=""

        subsuffix="Small"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix
        
        subsuffix="Medium"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Large"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        box = layout.box() #NEW BOX

        row=box.row()
        row.label(text="Color:", icon="COLOR")

        row=box.row()
        subsuffix="Gray"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="White"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Black"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        row=box.row()
        subsuffix="Red"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Green"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Blue"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        
        row=box.row()
        subsuffix="Yellow"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Orange"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Orange"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Purple"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        box = layout.box() #NEW BOX

        row=box.row()
        row.label(text="Class (Main):", icon="PMARKER_ACT")

        row=box.row()
        
        subsuffix="Base"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Raw"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix
                
        subsuffix="Main"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        box = layout.box() #NEW BOX

        row=box.row()
        row.label(text="Class (Sub):", icon="KEYFRAME_HLT")

        row=box.row()

        subsuffix="Extra"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Sub"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix
                
        subsuffix="Alt"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        box = layout.box() #NEW BOX

        row=box.row()
        row.label(text="Direction (Sky):", icon="OBJECT_ORIGIN")

        row=box.row()

        subsuffix="North"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="South"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix
                
        subsuffix="East"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="West"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        box = layout.box() #NEW BOX

        row=box.row()
        row.label(text="Direction (Relative):", icon="ORIENTATION_LOCAL")

        row=box.row()

        subsuffix="Top"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Bottom"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix
                
        subsuffix="Left"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Right"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix       

        box = layout.box() #NEW BOX

        row=box.row()
        row.label(text="Timestamp:", icon="TIME")

        row=box.row()

        subsuffix="Pre"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Current"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix
                
        subsuffix="After"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Later"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix  

        box = layout.box() #NEW BOX

        row=box.row()
        row.label(text="Marks:", icon="BOOKMARKS")

        row=box.row()

        subsuffix="New"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Temp"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix
                
        subsuffix="Placeholder"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Test"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix  

    
        box = layout.box() #NEW BOX

        row=box.row()
        row.label(text="Part:", icon="TRACKER")

        row=box.row()

        subsuffix="Beginn"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Middle"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix
                
        subsuffix="End"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

            
        box = layout.box() #NEW BOX

        row=box.row()
        row.label(text="State:", icon="PIVOT_BOUNDBOX")

        row=box.row()

        subsuffix="Open"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Closed"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix
                
        subsuffix="Exposed"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        box = layout.box() #NEW BOX

        row=box.row()
        row.label(text="Quality:", icon="META_DATA")

        row=box.row()

        subsuffix="Broken"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

        subsuffix="Damaged"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix
                
        subsuffix="Intact"
        op=row.operator(UVC_Operator_rename.bl_idname, text=subsuffix)
        op.PreFix=Tooldata_Renamer.Prefix
        op.Suffix=Tooldata_Renamer.Suffix
        op.Suffix_Sub=subsuffix

####################################################################################################
#06_menu_renamer_op.pymodule
####################################################################################################



####################################################################################################
#07_menu_uvopt_a.pymodule
####################################################################################################


#create another panel
class UVC_PT_extratools_6(uvc_extratoolpanel, bpy.types.Panel):
    bl_label = "UV Optimizer"
    bl_parent_id = "anifanpostuptools_PT_extratools"
    
    
    def draw(self, context):
        layout = self.layout
        box = layout.box() #NEW BOX
        row=box.row()
        
        settingsdata = bpy.context.scene.ttb_settings_data
        
        #create operator for UVC_Operator_createOptimizedUV
        row.operator(UVC_Operator_createOptimizedUV.bl_idname, text="Optimize UVs", icon='UV')
        

####################################################################################################
#07_menu_uvopt_op.pymodule
####################################################################################################

#import treathing
import threading

#Operator createOptimizedUV
class UVC_Operator_createOptimizedUV(bpy.types.Operator):
    """ OPERATOR
    Adds a Panel
    """
    bl_idname = "anifanpostuptools.createoptimizeduv"
    bl_label = "Create Optimized UV"
    
    def execute(self, context):
        bpy.ops.ed.undo_push(message="Create Optimized UV")
        #background_thread = threading.Thread(target= createOptimizedUV, args=(self, context))
        createOptimizedUV (self, context)
        #background_thread.start()
        return {'FINISHED'}


def createOptimizedUV(self, context):
    # Get active Objects
    selected_Objects = bpy.context.selected_objects

    # Select the objects you want to rename
    selected_objects = bpy.context.selected_objects
    for obj in selected_objects:
        #cache the old uv in a list of Islands
        uvIslands = []
        for uv in obj.data.uv_layers.active.data:
            uvIslands.append(uv.uv)
            
        #add new uv called "Optimized" if not exists
        if not "Optimized" in obj.data.uv_layers:
            obj.data.uv_layers.new(name="Optimized")
            
        #set the new uv to active
        obj.data.uv_layers.active = obj.data.uv_layers["Optimized"]
        
        #get all images that are used in the materials of the object
        images = []
        for slot in obj.material_slots:
            if slot.material:
                for node in slot.material.node_tree.nodes:
                    if node.type == "TEX_IMAGE":
                        if (node.image):
                            images.append(node.image)
                        
        #Create dicts for images, uvIslands and pixels parented to each other
        uvdict = {}
       
       

                        
        # Iterate all islands
        for i, uv in enumerate(uvIslands):
            imageDict = {}
            # Iterate all images
            for image in images:
                uvIslandDict = {
                    'image': image,
                    'pixels': {}             
                    
                }
                #iterate faces of the island
                
                
                #convert pixels into 2 dimensional array make sure the array has the same pixel position as the uvs
                pixels = []
                # Get the actual dimensions of the image
                height, width = image.size

                # Convert pixels into 3 dimensional array (height, width, RGBA)
                pixels = np.array(image.pixels).reshape(width, height, 4)
                
                size= height * width
                                                
             
                #iterate x and y of the pixels
                for x in range(width):
                    for y in range(height):
                        pixelDict = {
                            'top': 0,
                            'bottom': 0,
                            'left': 0,
                            'right': 0,
                            
                            #average difference of the top, bottom, left and right pixel
                            'average': 0,
                            
                            #3D vector
                            'orientation': {
                                'x': 0,
                                'y': 0
                            },
                            'straigthness': 0
                            
                        }
                        pixel = int (pixels[x][y][0] + pixels[x][y][1] + pixels[x][y][2]) / 3
                        
                        
                       
                        #add the difference to the top , bottom , left and right pixel to a variable   
                        if y+1 < height:
                            top =  pixel -  getpixelgrayscaled(getpixelfromArray(pixels, x, y+1))
                        else:
                            top = pixel  # or some other default value
                            
                        
                        if y-1 >= 0:
                            bottom =  pixel - getpixelgrayscaled(getpixelfromArray(pixels, x, y-1))
                        else:
                            bottom = pixel  # or some other default value
                            
                        if x-1 >= 0:
                            left =  pixel - getpixelgrayscaled(getpixelfromArray(pixels, x-1, y))
                        else:
                            left = pixel  # or some other default value
                            
                        if x+1 < width:
                            right =  pixel - getpixelgrayscaled(getpixelfromArray(pixels, x+1, y))
                        else:
                            right = pixel  # or some other default value
                            
                                   
                        difference = top + bottom + left + right
                        difference = difference / 4
                        

                        orientation = (top - bottom, left - right)
                        norm = np.linalg.norm(orientation)
                        orientation = (orientation[0] / norm, orientation[1] / norm)
                        straigthness =  abs(0.5 - (abs(top) + abs(bottom) + abs(left) + abs(right)) / 4)
                        
                        #add the differences to the pixelDict
                        pixelDict['top'] = top
                        pixelDict['bottom'] = bottom
                        pixelDict['left'] = left
                        pixelDict['right'] = right
                        
                        #add the average difference to the pixelDict
                        pixelDict['average'] = difference
                        
                        #add the orientation to the pixelDict
                        pixelDict ['orientation'].update( {'x': orientation[0] })
                        pixelDict['orientation'].update( {'y': orientation[1] })
                        
                        # Add the straigthness to the pixelDict
                        pixelDict['straigthness'] = straigthness
                                           
                        uvIslandDict['pixels']['p'+ str(x) +"/"+ str(y)] = pixelDict.copy()
                        
                        
                        
                    #cacululate the average orientation of all pixels 
                    averageOrientation = (0, 0)
                    straigthness=0
                    mindifference=0
                    maxdifference=0
                    
                    for pixdata in uvIslandDict['pixels'].values():
                        orientationdict = pixdata['orientation']
                        
                        orientationx = orientationdict['x']
                        orientationy = orientationdict['y']
                                        
                        #add the orientation to the average orientation
                        averageOrientation = (averageOrientation[0] + orientationx, averageOrientation[1] + orientationy)
                        
                        #calculate how much the vectors are straight to left or right or top or bottom
                        #substract them to get how much the vectors are, the closer to 0.5 the less straight they are
                        
                # Add the imageDict to the uvdict using update
                uvdict.update(imageDict)
                
                #Create image from uvdict
                # Create a new image
                new_image = bpy.data.images.new("Optimized", width=size, height=size)
                # Create a new pixels array
                new_pixels = []
                
                # Iterate all pixels
                for x in range(size):
                    for y in range(size):
                        # Get the pixel from the uvdict
                        key = 'p'+ str(x) +"/"+ str(y)
                        if key in uvdict:
                            pixeldata = uvdict[key]
                            new_pixels.append(pixeldata['average'])
                        else:
                            new_pixels.append(255)
                        
                        
                        
                        
def getpixelgrayscaled(pixel):
    return int (pixel[0] + pixel[1] + pixel[2]) / 3

def getpixelfromArray(array, x, y):
    return array[x][y]
                        

                    

                    
#MODULE_EARLY_INSTALLERSPACE_START_00000000
    



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




''' DEPRECATED SIDELOADER; USE MODULE INSTALL SCRIPT INSTEAD!
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
def get_vertexpositiondata_by_id(vertex_group_data, vertex_id):
(): return None
def get_vertexpositiondata_by_id(vertex_group_data, vertex_id):
(): return None

# Now you can use testfunc directly
def sideloader():

    #Functionimport:
    print("SIDELOAD START")

    #get Directory
    current_directory = os.path.dirname(__file__)
    
    addons_directory = os.path.join(current_directory, 'addons')#added for functionbuffering

    #get Python files
    files = find_python_files(current_directory)
    
    # Use os.path.join to create the full path to the file
    function_file_path = os.path.join(addons_directory, 'function_names.py')

    #fileblacklist
    fileblacklist = ["__init__.py", "auto_load.py", "animationpostupstools.py", "function_names.py", "function_names.py"]
    
    with open(function_file_path, 'w') as function_file: #added for functionbuffering
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
                
                # Write the function name to the new file
                function_file.write(f'def {function_name}(): pass\n') #added for functionbuffering

    print ("SIDELOAD END")

#Tester
sideloader()
sideloadtester()


'''


#Generic Tools Data:

def splitNormals_dummy(self, context):
    splitNormals(self, context)

class TTB_Data_Settings(bpy.types.PropertyGroup):
    """Stores Settings"""

    extendsplitnormalmenu: bpy.props.BoolProperty(name="Expand",description="Expand more Buttons",default=True)

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
    

####################################################################################################
#18_operators_debug.pymodule
####################################################################################################




 

def debug_write_vertex_coordinated(self, context):
        # Get the selected object
    obj = context.object
    
    # Check if the selected object is a mesh
    if obj and obj.type == 'MESH':
        # Get the mesh data
        mesh = obj.data
        
        # Iterate over all vertices and print their positions
        for vertex in mesh.vertices:
            print(f"Vertex {vertex.index}: {vertex.co}")
            
def debug_setupBone(self, context):
    # Get the selected object
    obj = context.object
    
    armature = createArmatureifNotExists(bpy.context, obj)
    centerposition = convert_to_armature_space(armature, Vector((0, 0, 0)), obj)
    groupname, group= createIncrementedVertexgroupIfNotExists(obj, "root_base")
    bone = createBoneifNotExists(armature, groupname, centerposition)
    vertex_indices = getAllVertexIndices(obj)
    applyVertexgroupToMesh(obj, groupname, vertex_indices)
    
    # Check if the selected object is a mesh
    if obj and obj.type == 'MESH':
        # Get the mesh data
        mesh = obj.data
        
        # Iterate over all vertices and print their positions
        for vertex in mesh.vertices:
            # Apply the bone's matrix to the vertex position
            transformed_position = bone.matrix @ vertex.co
            print(f"Vertex {vertex.index}: {transformed_position}")

def debug_print_vertex_withBoneAnimation(self, context):
    # Get the selected object
    obj = context.object
    if obj and obj.type == 'MESH':
        armature = createArmatureifNotExists(bpy.context, obj)
        centerposition = convert_to_armature_space(armature, Vector((0, 0, 0)), obj)
        groupname, group= createIncrementedVertexgroupIfNotExists(obj, "root_base")
        bone = createBoneifNotExists(armature, groupname, centerposition)
        vertex_indices = getAllVertexIndices(obj)
        applyVertexgroupToMesh(obj, groupname, vertex_indices)
        matrix=getMatrixOfAnimation_PoseBonespace(obj, armature, group)
        
        positions = getPositionFromIndices(obj, vertex_indices)
        
        animated_positions=multiply_matrix(matrix, positions)
        print ("Single Bone Animation: "+str(animated_positions))
        
        fullyanimated_positions=apply_transformations (obj, armature, vertex_indices, animated_positions)
        print ("Full Animation: "+str(fullyanimated_positions))
        
def debug_print_applyAnimation(self, context):
    # Get the selected object
    obj = context.object
    if obj and obj.type == 'MESH':
        armature = createArmatureifNotExists(bpy.context, obj)
        centerposition = convert_to_armature_space(armature, Vector((0, 0, 0)), obj)
        groupname, group= createIncrementedVertexgroupIfNotExists(obj, "root_base")
        bone = createBoneifNotExists(armature, groupname, centerposition)
        vertex_indices = getAllVertexIndices(obj)
        applyVertexgroupToMesh(obj, groupname, vertex_indices)
        matrix=getMatrixOfAnimation_PoseBonespace(obj, armature, group)
        
        positions = getPositionFromIndices(obj, vertex_indices)
        
        animated_positions=multiply_matrix(matrix, positions)
        print ("Single Bone Animation: "+str(animated_positions))
        
        fullyanimated_positions=apply_transformations (obj, armature, vertex_indices, animated_positions)
        print ("Full Animation: "+str(fullyanimated_positions))
        
        set_vertex_positions_4dsafe(obj, vertex_indices, fullyanimated_positions)
        removeArmatureAndVertexgroups (obj, armature)
        set_vertex_positions_4dsafe(obj, vertex_indices, fullyanimated_positions)
        
        
        

####################################################################################################
#19_operators_generic.pymodule
####################################################################################################



####################################################################################################
#20_module_bl_current_obj_getters.pymodule
####################################################################################################

def get_current_Vertcount():
    """ !FUNCTION!
    Returns the Amount of Vertices in the Current Mesh
    
    :return: Amount of Vertices in the Current Mesh
    :rtype: int
    """
    functionname="GETCURRENTVERTCOUNT"
    mesh = bpy.context.object.data
    if mesh:
        return len(mesh.vertices)
    else:
        return 0

####################################################################################################
#21_module_op_pivot.pymodule
####################################################################################################

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

####################################################################################################
#22_module_bl_selector.pymodule
####################################################################################################

def setSelectionforAllObjects(selected_Objects, state):
    for obj in selected_Objects:
        obj.select_set(state) 
    bpy.context.view_layer.update()              

####################################################################################################
#30_module_bl_image.pymodule
####################################################################################################

def linear_to_sRGB(linear_value):
    if linear_value <= 0.0031308:
        sRGB_value = 12.92 * linear_value
    else:
        sRGB_value = 1.055 * (linear_value ** (1/2.4)) - 0.055
    return sRGB_value

def math_UVPosition_By_Tile(xt, yt, tile_count_x, tile_count_y):
    
    """  !METHOD!
    Divides the UV into Tiles based on Tilecount and gets the Center Position of that Square

    Keyword arguments:
    :param int xt,yt:                       Squareposition
    :param: int tile_count_x,tile_count_y:  Amount of Squares per Axies
    :return: float uv_x, uv_y:              Postion on UV 0.0-1.0
    """

    
    uv_x = (xt / tile_count_x) + (0.5 / tile_count_x)
    uv_y = (yt / tile_count_y) + (0.5 / tile_count_y)
    
    #Add Debug Here?

    return uv_x, uv_y

def math_PixelIndex_By_TileNumber(xt, yt, width, height, tile_count_x, tile_count_y, uv_offset_x=0, uv_offset_y=0):
    """ !METHOD! 
    Uses the Sizes of the Texture, the Tilecount and Calculates the Index of the Pixel in the Array

    Keyword arguments:
    :param int xt,yt:                       Squareposition
    :param float width,height:              Size of Image
    :param: int tile_count_x,tile_count_y:  Amount of Squares per Axies
    :return: int index:                     index of Pixel inside a Array
    """
        
    mid_x = (xt * width // tile_count_x) + (width // tile_count_x // 2) + int(uv_offset_x)
    mid_y = (yt * height // tile_count_y) + (height // tile_count_y // 2) + int(uv_offset_y)
    index = (mid_y * width + mid_x) * 4

    functionname="CalculateMiddlePixel"

    printLog(src=functionname, msg="xt: " + str(xt) + " yt: " + str(yt) + " width: " + str(width) + " height: " + str(height) + " tile_count_x: " + str(tile_count_x) + " tile_count_y: " + str(tile_count_y) + " uv_offset_x: " + str(uv_offset_x) + " uv_offset_y: " + str(uv_offset_y), subtype=LOGTYPE.IN)
    printLog(src=functionname, msg="index: " + str(index), subtype=LOGTYPE.OUT)
     
    return index 
    
def math_getTileFromUVXY(tilecountx, tilecounty, x,y):    
    
    """ !METHOD!
    Calculates the Basetile from the Tilecount and the UV Coordinate

    Keyword arguments:
    xxx                       N/A #
    """


    segment_x = int(min(math.floor(x * tilecountx), tilecountx - 1))
    segment_y = int(min(math.floor(y * tilecounty), tilecounty - 1))
    #printLog(src="calculateSegment", subtype=LOGTYPE.INFO, msg="Segmentcoordinates"+str(segment_x)+"/"+str(segment_y)) 
    
    return segment_x,segment_y  
   
def math_getTileFromUV(tilecountx, tilecounty, uv):
    """ !METHOD!
    Calculates the Basetile from the Tilecount and the UV Coordinate

    Keyword arguments:
    xxx                       N/A #
    """



    segment_x = int(min(math.floor(uv.x * tilecountx), tilecountx - 1))
    segment_y = int(min(math.floor(uv.y * tilecounty), tilecounty - 1))
    #printLog(src="calculateSegment", subtype=LOGTYPE.INFO, msg="Segmentcoordinates"+str(segment_x)+"/"+str(segment_y)) 
    
    return segment_x,segment_y  

def img_readPixel_By_Index(img, index):
    """ !METHOD!
    Gets the Color of a Pixel inside a Pixel Array of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    return img.pixels[index:index + 4]

def readImagePixel(image, x, y):
    """ !METHOD!
    Reads the Pixel Data of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    
    width = image.size[0]
    height = image.size[1]
    
    index = img_getImagePixelIndex(x, y, width)
    pixels=image.pixels[index:index + 4]
    
    return pixels

def img_getImagePixelIndex(xt, yt, imagewidth):
    """ !METHOD!
    Gets the Color of a Pixel inside a Pixel Array of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    
    return (yt * imagewidth + xt)*4

def img_getTilesetPixelIndex(xt, yt, tilesizex):
    """ !METHOD!
    Gets the Color of a Pixel inside a Pixel Array of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    
    return yt * (tilesizex) + xt 

def math_getIndexByTile(xt, yt, tile_count_x):
    
    return yt * tile_count_x + xt

####################################################################################################
#40_module_bl_normals.pymodule
####################################################################################################

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


####################################################################################################
#50_module_bl_rotationtool.pymodule
####################################################################################################

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

####################################################################################################
#60_module_bl_uvs.pymodule
####################################################################################################



####################################################################################################
#70_module_bl_vertexgroups.pymodule
####################################################################################################

                
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



#Used by UVC_Operator_selectByGroup from
def selectByGroup(self, ctx):
    
    activeobj = ctx.active_object
    me = activeobj.data
    bm = bmesh.from_edit_mesh(me)

    # Iterate through faces to find selected ones
    active_face_index = None
    
    for face in bm.faces:
        for element in reversed(bm.select_history):
            if isinstance(element, bmesh.types.BMFace):
                face = element
                break

        if face is None: 
            return (None)
        if face.select and active_face_index is None:
            active_face_index = face.index

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
        
    if active_face_index is not None:
        # Update the BMesh data
        bm = bmesh.from_edit_mesh(me)
        # Update the internal index table
        bm.faces.ensure_lookup_table()   
        # Select the active face
        bm.select_history.add( bm.faces[active_face_index])
            
            

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
    # Switch to vertex select mode
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_mode(type='FACE')



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

####################################################################################################
#71_module_bl_vertexmanipulation.pymodule
####################################################################################################


def getAllVertexIndices(obj):
    return [vertex.index for vertex in obj.data.vertices]    

def getPositionFromIndices(obj, vertex_indices):
    return [obj.data.vertices[index].co for index in vertex_indices]

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
 
def set_vertex_positions_4dsafe(obj, vertex_indices, positions):
    # Iterate over the vertex indices
    for index, vertex_index in enumerate(vertex_indices):
        # Get the position
        position = positions[index]
        
        # Check if the position has 4 items
        if len(position) == 4:
            # Remove the last item
            position = position[:3]
        
        # Set the vertex position
        obj.data.vertices[vertex_index].co = position 

####################################################################################################
#80_module_bl_animation.pymodule
####################################################################################################


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


####################################################################################################
#81_module_bl_armatures.pymodule
####################################################################################################


  
#Getters  
        
def checkIfBoneExists(armature, bone_name):
    if armature.type != 'ARMATURE':
        return None
    # Check if the bone already exists in the armature
    return bone_name in armature.data.edit_bones

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

#Cleanup

def removeArmatureAndVertexgroups(obj, armature):
    # Check if the armature is the parent of the object
    if obj.parent == armature:
        # Remove the parent-child relationship
        obj.parent = None
        obj.matrix_parent_inverse = armature.matrix_world.inverted()
    
    # Remove all vertex groups associated with the object
    remove_vertex_groups(obj)
    
    # Remove the armature object
    bpy.data.objects.remove(armature, do_unlink=True)

def removeArmatureifExists(context, mesh):
    # Check if an armature with the same name already exists
    armature_name = mesh.name + "_armature"
    if armature_name in bpy.data.objects:
        # Remove the armature object
        bpy.data.objects.remove(bpy.data.objects[armature_name], do_unlink=True)
        print(f"Removed armature {armature_name}.")

#Autocreate Bones/Armatures (Bonefunctions need to be merged)
def apply_transformations(obj, armature, vertex_indices, positions):
    # Create a copy of the positions list to store the transformed positions
    transformed_positions = positions.copy()
    
    # Get the armature's pose bones
    pose_bones = armature.pose.bones
    
    # Iterate over the vertex indices and positions
    for i, vertex_index in enumerate(vertex_indices):
        # Get the vertex position
        vertex_position = positions[i]
        
        # Convert the vertex position to armature space
        vertex_position_armature_space = convert_to_armature_space(armature, vertex_position, obj)
        
        # Apply the transformations for each bone affecting the vertex
        for bone in pose_bones:
            # Get the vertex group associated with the bone
            vertex_group = obj.vertex_groups.get(bone.name)
            
            # Check if the vertex group exists and the vertex is in the vertex group
            if vertex_group and vertex_index in [g.group for g in obj.data.vertices[vertex_index].groups if g.group == vertex_group.index]:
                # Get the weight of the bone affecting the vertex
                weight = next((g.weight for g in obj.data.vertices[vertex_index].groups if g.group == vertex_group.index), 0)
                
                # Apply the bone's transformation to the vertex position
                transformed_position = vertex_position_armature_space @ bone.matrix @ bone.matrix_basis.inverted()
                
                # Apply the weight to the transformed position
                transformed_position *= weight
                
                # Convert the transformed position back to object space
                transformed_position_object_space = armature.matrix_world @ transformed_position
                
                # Update the transformed position in the list
                transformed_positions[i] = transformed_position_object_space
    
    # Return the transformed positions
    return transformed_positions


#Creators

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


#Get Positions

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

#get Matrix of Animation
def getMatrixOfAnimation_PoseBonespace(obj, armature, groupbone):
    # Get the current frame
    current_frame = bpy.context.scene.frame_current
    
    armaturePosMode(armature, obj)
    
    # Select the armature object
    bpy.context.view_layer.objects.active = armature
    
    # Switch to pose mode to access bone transformations
    bpy.ops.object.mode_set(mode='POSE')
    
    # Get the pose bone corresponding to the groupbone
    pose_bone = armature.pose.bones.get(groupbone.name)
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    objectEditMode(obj)
    
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




####################################################################################################
#99_modlule_kd_important_getters.pymodule
####################################################################################################

#test
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
    """Tool storage for Bonery module"""
    my_tool: bpy.props.PointerProperty(type=bpy.types.Object, name="My Tool")
    key_data: bpy.props.CollectionProperty(type=Keydata, name="Key Data")
    active_keydata : bpy.props.IntProperty(name="Active Index", default=0)


class Tooldata_Renamer(bpy.types.PropertyGroup):
    """Tool storage for Renamer module"""
    Prefix : bpy.props.StringProperty(name="Prefix", default="")
    Suffix : bpy.props.StringProperty(name="Suffix", default="")


#Function Importer

#MODULE_INSTALLER_SPACE_END_00000001

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
    setattr(bpy.types.Scene, "bonery_tools_data_renamer", bpy.props.PointerProperty(name="UV Palettes settings data", type=Tooldata_Renamer))
    setattr(bpy.types.Scene, "bonery_vertex_group_data", bpy.props.PointerProperty(name="UV Palettes settings data", type=VertexGroupData))
    setattr(bpy.types.Scene, "bonery_vertex_position_data", bpy.props.PointerProperty(name="UV Palettes settings data", type=VertexPositionData))
    #Generic Tools
    setattr(bpy.types.Scene, "ttb_settings_data", bpy.props.PointerProperty(name="Generic Tools settings data", type=TTB_Data_Settings))

    # tool_auto_group_selector
    # AutoGroupSelector
    
    #Register the tool using setattribute
    #setattr(bpy.types, "tool_auto_group_selector", AutoGroupSelector)
    bpy.utils.register_tool(AutoGroupSelector, after={"builtin.select_box"})
    bpy.utils.register_tool(AutoGroupSelectorObject, after={"builtin.select_box"})


# Ignore section


# def import_functions_from_file(file_name):
#     print("running import_functions_from_file")
#     current_directory = os.path.dirname(__file__)
#     file_path = os.path.join(current_directory, file_name)
    
#     # Load the spec and module from the file path
#     spec = importlib.util.spec_from_file_location("module.name", file_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
    
