bl_info = {
    "name": "Export NURBS Curve to JSON",
    "blender": (2, 80, 0),
    "category": "Import-Export",
    "description": "Exports NURBS Curve data to a JSON file",
    "author": "Mark Nguyen",
    "version": (1, 0, 0),
    "doc_url": "https://github.com/canxerian/blender-nurb-curve-to-json",
    "location": "Export > Export NURBS Curve to JSON",
}

import bpy
import json
import os

class ExportNURBCurveToJSON(bpy.types.Operator):
    """Export NURBS Curve to JSON"""
    bl_idname = "export.nurb_curve_to_json"
    bl_label = "Export NURBS Curve to JSON"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # Get the active object
        obj = context.object
        if not obj or obj.type != 'CURVE':
            self.report({'ERROR'}, "No active NURBS curve object")
            return {'CANCELLED'}
        
        curve = obj.data
        
        # Check if it is a NURBS curve
        if curve.splines[0].type != 'NURBS':
            self.report({'ERROR'}, "Active curve is not a NURBS curve")
            return {'CANCELLED'}
        
        # Extract NURBS curve data
        nurb_data = []
        for spline in curve.splines:
            if spline.type == 'NURBS':
                points = []
                for point in spline.points:
                    points.append({
                        'x': point.co.x,
                        'y': point.co.y,
                        'z': point.co.z,
                        'w': point.co.w,
                        'weight': point.weight
                    })
                nurb_data.append({
                    'order_u': spline.order_u,
                    'points': points,
                })
        
        # Convert to JSON
        nurb_json = json.dumps(nurb_data, indent=4)
        
        # Save JSON to file
        with open(self.filepath, 'w') as f:
            f.write(nurb_json)
        
        self.report({'INFO'}, "NURBS curve exported successfully")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func_export(self, context):
    self.layout.operator(ExportNURBCurveToJSON.bl_idname, text="NURBS Curve to JSON")

def register():
    bpy.utils.register_class(ExportNURBCurveToJSON)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportNURBCurveToJSON)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
