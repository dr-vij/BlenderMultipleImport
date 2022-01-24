import bpy

def read_objects_to_scene(context, directory, files):
    import os
    for file in files:
        path = os.path.join(directory, file.name)
        if file.name.endswith(".obj"):
            bpy.ops.import_scene.obj(filepath=path)
        if file.name.endswith(".fbx"):
            bpy.ops.import_scene.fbx(filepath=path)
            
    return {'FINISHED'}

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator


class MultipleFilesImporter(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "importer.import_files"  # important since its how bpy.ops.importer.import_files is constructed
    bl_label = "Import files"

    # ImportHelper mixin class uses this
    filename_ext = ".obj;.fbx"

    filter_glob: StringProperty(
        default="*.obj;*.fbx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    #get directory to combine it with files
    directory: StringProperty(subtype='DIR_PATH')
    
    #get multiple files here
    files: CollectionProperty(
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'},
    )

    def execute(self, context):
        return read_objects_to_scene(context, self.directory, self.files)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(MultipleFilesImporter.bl_idname, text="Import Multiple Files")

# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access)
def register():
    if not hasattr(bpy.types, bpy.ops.importer.import_files.idname()):
        bpy.utils.register_class(MultipleFilesImporter)
        bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(MultipleFilesImporter)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.importer.import_files('INVOKE_DEFAULT')
