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

if __name__ == "__main__":
    createEmpty('CreateEmpty',0.5,'ARROWS')
