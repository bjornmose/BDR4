import bpy


'''
wrapper to create Epmties along the 'python API debelopers moods'
'''

def createEmpty(OName,draw_size,draw_type):
    #print('Create {:}'.format(OName))
    Cobj = bpy.data.objects.new( OName, None )
    ver = bpy.app.version[1]
    ver0 = bpy.app.version[0]
    #print(ver)
    if (ver < 80 and ver0 < 3):
        bpy.context.scene.objects.link( Cobj )
        Cobj.empty_draw_size = draw_size
        Cobj.empty_draw_type = draw_type
        Cobj.show_name=1
    
    if (ver > 79 and ver0 < 3):
        bpy.context.scene.collection.objects.link( Cobj )
        Cobj.empty_display_size = draw_size
        Cobj.empty_display_type = draw_type
        Cobj.show_name=1

    if (ver < 99 and ver0 > 2):
        view_layer = bpy.context.view_layer
        view_layer.active_layer_collection.collection.objects.link( Cobj )
        Cobj.empty_display_size = draw_size
        Cobj.empty_display_type = draw_type
        Cobj.show_name=1

    return Cobj   

def deleteObject35(name):
    try:
        objs = [bpy.context.scene.objects[name]]
        with bpy.context.temp_override(selected_objects=objs):
            bpy.ops.object.delete()
        return('FINISHED')

    except:
        print('NOT Deleted',name)
        return('FAILED')
    
    
def deleteObject(name):
    obj = bpy.data.objects.get(name)
    ver = bpy.app.version[1]
    ver0 = bpy.app.version[0]
    #print(ver)
    if (ver < 80 and ver0 < 3):
     if (obj is not None):
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        # Select the object
        bpy.data.objects[name].select = True    # Blender 2.7x        
        # Delete the object
        bpy.ops.object.delete() 
        print('deleted',name)
        return('FINISHED')
        
    if (ver < 99 and ver0 > 2):
     try:
        objs = [bpy.context.scene.objects[name]]
        with bpy.context.temp_override(selected_objects=objs):
            bpy.ops.object.delete()
        return('FINISHED')
     except:
        print('NOT Deleted',name)
        return('FAILED')


    
    

if __name__ == "__main__":
    createEmpty('CreateEmpty',0.5,'ARROWS')
