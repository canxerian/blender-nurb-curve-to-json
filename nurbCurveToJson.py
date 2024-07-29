bl_info = {
    "name": "Export NURB Curve to JSON",
    "blender": (4, 20, 0),
    "category": "Import-Export",
    "description": "1. Create NURB Curve, 2. Export > NURB Curve to JSON, 3. Use data in 3D engine, e.g three.js",
    "author": "Mark Nguyen",
    "version": (1, 0, 0),
    "doc_url": "https://github.com/canxerian/blender-nurb-to-json",
    "support": "https://github.com/canxerian/blender-nurb-to-json/issues",
    "location": "Export > Export NURB Curve to JSON"
}

import bpy
import json
import os

class ExportNURBCurveToJSON(bpy.types.Operator):
    """Export NURB Curve to JSON"""
    bl_idname = "export.nurb_curve_to_json"
    bl_label = "Export NURB Curve to JSON"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # Get the active object
        obj = context.object
        if not obj or obj.type != 'CURVE':
            self.report({'ERROR'}, "No active NURB curve object")
            return {'CANCELLED'}
        
        curve = obj.data
        
        # Check if it is a NURB curve
        if curve.splines[0].type != 'NURBS':
            self.report({'ERROR'}, "Active curve is not a NURB curve")
            return {'CANCELLED'}
        
        # Extract NURB curve data
        nurb_data = []
        for spline in curve.splines:
            if spline.type == 'NURBS':
                points = []
                for point in spline.points:
                    points.append({
                        'co': [point.co.x, point.co.y, point.co.z, point.co.w],
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
        
        self.report({'INFO'}, "NURB curve exported successfully")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func_export(self, context):
    self.layout.operator(ExportNURBCurveToJSON.bl_idname, text="NURB Curve to JSON")

def register():
    bpy.utils.register_class(ExportNURBCurveToJSON)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportNURBCurveToJSON)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
