
import bpy
from mathutils import Matrix, Vector
from math import acos, pi

rig_id = "ars6fpc607256a55"


############################
## Math utility functions ##
############################

def perpendicular_vector(v):
    """ Returns a vector that is perpendicular to the one given.
        The returned vector is _not_ guaranteed to be normalized.
    """
    # Create a vector that is not aligned with v.
    # It doesn't matter what vector.  Just any vector
    # that's guaranteed to not be pointing in the same
    # direction.
    if abs(v[0]) < abs(v[1]):
        tv = Vector((1,0,0))
    else:
        tv = Vector((0,1,0))

    # Use cross prouct to generate a vector perpendicular to
    # both tv and (more importantly) v.
    return v.cross(tv)


def rotation_difference(mat1, mat2):
    """ Returns the shortest-path rotational difference between two
        matrices.
    """
    q1 = mat1.to_quaternion()
    q2 = mat2.to_quaternion()
    angle = acos(min(1,max(-1,q1.dot(q2)))) * 2
    if angle > pi:
        angle = -angle + (2*pi)
    return angle


#########################################
## "Visual Transform" helper functions ##
#########################################

def get_pose_matrix_in_other_space(mat, pose_bone):
    """ Returns the transform matrix relative to pose_bone's current
        transform space.  In other words, presuming that mat is in
        armature space, slapping the returned matrix onto pose_bone
        should give it the armature-space transforms of mat.
        TODO: try to handle cases with axis-scaled parents better.
    """
    rest = pose_bone.bone.matrix_local.copy()
    rest_inv = rest.inverted()
    if pose_bone.parent:
        par_mat = pose_bone.parent.matrix.copy()
        par_inv = par_mat.inverted()
        par_rest = pose_bone.parent.bone.matrix_local.copy()
    else:
        par_mat = Matrix()
        par_inv = Matrix()
        par_rest = Matrix()

    # Get matrix in bone's current transform space
    smat = rest_inv * (par_rest * (par_inv * mat))

    # Compensate for non-local location
    #if not pose_bone.bone.use_local_location:
    #    loc = smat.to_translation() * (par_rest.inverted() * rest).to_quaternion()
    #    smat.translation = loc

    return smat


def get_local_pose_matrix(pose_bone):
    """ Returns the local transform matrix of the given pose bone.
    """
    return get_pose_matrix_in_other_space(pose_bone.matrix, pose_bone)


def set_pose_translation(pose_bone, mat):
    """ Sets the pose bone's translation to the same translation as the given matrix.
        Matrix should be given in bone's local space.
    """
    if pose_bone.bone.use_local_location is True:
        pose_bone.location = mat.to_translation()
    else:
        loc = mat.to_translation()

        rest = pose_bone.bone.matrix_local.copy()
        if pose_bone.bone.parent:
            par_rest = pose_bone.bone.parent.matrix_local.copy()
        else:
            par_rest = Matrix()

        q = (par_rest.inverted() * rest).to_quaternion()
        pose_bone.location = q * loc


def set_pose_rotation(pose_bone, mat):
    """ Sets the pose bone's rotation to the same rotation as the given matrix.
        Matrix should be given in bone's local space.
    """
    q = mat.to_quaternion()

    if pose_bone.rotation_mode == 'QUATERNION':
        pose_bone.rotation_quaternion = q
    elif pose_bone.rotation_mode == 'AXIS_ANGLE':
        pose_bone.rotation_axis_angle[0] = q.angle
        pose_bone.rotation_axis_angle[1] = q.axis[0]
        pose_bone.rotation_axis_angle[2] = q.axis[1]
        pose_bone.rotation_axis_angle[3] = q.axis[2]
    else:
        pose_bone.rotation_euler = q.to_euler(pose_bone.rotation_mode)


def set_pose_scale(pose_bone, mat):
    """ Sets the pose bone's scale to the same scale as the given matrix.
        Matrix should be given in bone's local space.
    """
    pose_bone.scale = mat.to_scale()


def match_pose_translation(pose_bone, target_bone):
    """ Matches pose_bone's visual translation to target_bone's visual
        translation.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_translation(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


def match_pose_rotation(pose_bone, target_bone):
    """ Matches pose_bone's visual rotation to target_bone's visual
        rotation.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_rotation(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


def match_pose_scale(pose_bone, target_bone):
    """ Matches pose_bone's visual scale to target_bone's visual
        scale.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_scale(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


##############################
## IK/FK snapping functions ##
##############################

def match_pole_target(ik_first, ik_last, pole, match_bone, length):
    """ Places an IK chain's pole target to match ik_first's
        transforms to match_bone.  All bones should be given as pose bones.
        You need to be in pose mode on the relevant armature object.
        ik_first: first bone in the IK chain
        ik_last:  last bone in the IK chain
        pole:  pole target bone for the IK chain
        match_bone:  bone to match ik_first to (probably first bone in a matching FK chain)
        length:  distance pole target should be placed from the chain center
    """
    a = ik_first.matrix.to_translation()
    b = ik_last.matrix.to_translation() + ik_last.vector

    # Vector from the head of ik_first to the
    # tip of ik_last
    ikv = b - a

    # Get a vector perpendicular to ikv
    pv = perpendicular_vector(ikv).normalized() * length

    def set_pole(pvi):
        """ Set pole target's position based on a vector
            from the arm center line.
        """
        # Translate pvi into armature space
        ploc = a + (ikv/2) + pvi

        # Set pole target to location
        mat = get_pose_matrix_in_other_space(Matrix.Translation(ploc), pole)
        set_pose_translation(pole, mat)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='POSE')

    set_pole(pv)

    # Get the rotation difference between ik_first and match_bone
    angle = rotation_difference(ik_first.matrix, match_bone.matrix)

    # Try compensating for the rotation difference in both directions
    pv1 = Matrix.Rotation(angle, 4, ikv) * pv
    set_pole(pv1)
    ang1 = rotation_difference(ik_first.matrix, match_bone.matrix)

    pv2 = Matrix.Rotation(-angle, 4, ikv) * pv
    set_pole(pv2)
    ang2 = rotation_difference(ik_first.matrix, match_bone.matrix)

    # Do the one with the smaller angle
    if ang1 < ang2:
        set_pole(pv1)


def fk2ik_arm(obj, fk, ik):
    """ Matches the fk bones in an arm rig to the ik bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    uarm  = obj.pose.bones[fk[0]]
    farm  = obj.pose.bones[fk[1]]
    hand  = obj.pose.bones[fk[2]]
    uarmi = obj.pose.bones[ik[0]]
    farmi = obj.pose.bones[ik[1]]
    handi = obj.pose.bones[ik[2]]

    # Stretch
    if handi['auto_stretch'] == 0.0:
        uarm['stretch_length'] = handi['stretch_length']
    else:
        diff = (uarmi.vector.length + farmi.vector.length) / (uarm.vector.length + farm.vector.length)
        uarm['stretch_length'] *= diff

    # Upper arm position
    match_pose_rotation(uarm, uarmi)
    match_pose_scale(uarm, uarmi)

    # Forearm position
    match_pose_rotation(farm, farmi)
    match_pose_scale(farm, farmi)

    # Hand position
    match_pose_rotation(hand, handi)
    match_pose_scale(hand, handi)


def ik2fk_arm(obj, fk, ik):
    """ Matches the ik bones in an arm rig to the fk bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    uarm  = obj.pose.bones[fk[0]]
    farm  = obj.pose.bones[fk[1]]
    hand  = obj.pose.bones[fk[2]]
    uarmi = obj.pose.bones[ik[0]]
    farmi = obj.pose.bones[ik[1]]
    handi = obj.pose.bones[ik[2]]
    pole  = obj.pose.bones[ik[3]]

    # Stretch
    handi['stretch_length'] = uarm['stretch_length']

    # Hand position
    match_pose_translation(handi, hand)
    match_pose_rotation(handi, hand)
    match_pose_scale(handi, hand)

    # Pole target position
    match_pole_target(uarmi, farmi, pole, uarm, (uarmi.length + farmi.length))


def fk2ik_leg(obj, fk, ik):
    """ Matches the fk bones in a leg rig to the ik bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    thigh  = obj.pose.bones[fk[0]]
    shin   = obj.pose.bones[fk[1]]
    foot   = obj.pose.bones[fk[2]]
    mfoot  = obj.pose.bones[fk[3]]
    thighi = obj.pose.bones[ik[0]]
    shini  = obj.pose.bones[ik[1]]
    footi  = obj.pose.bones[ik[2]]
    mfooti = obj.pose.bones[ik[3]]

    # Stretch
    if footi['auto_stretch'] == 0.0:
        thigh['stretch_length'] = footi['stretch_length']
    else:
        diff = (thighi.vector.length + shini.vector.length) / (thigh.vector.length + shin.vector.length)
        thigh['stretch_length'] *= diff

    # Thigh position
    match_pose_rotation(thigh, thighi)
    match_pose_scale(thigh, thighi)

    # Shin position
    match_pose_rotation(shin, shini)
    match_pose_scale(shin, shini)

    # Foot position
    mat = mfoot.bone.matrix_local.inverted() * foot.bone.matrix_local
    footmat = get_pose_matrix_in_other_space(mfooti.matrix, foot) * mat
    set_pose_rotation(foot, footmat)
    set_pose_scale(foot, footmat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


def ik2fk_leg(obj, fk, ik):
    """ Matches the ik bones in a leg rig to the fk bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    thigh    = obj.pose.bones[fk[0]]
    shin     = obj.pose.bones[fk[1]]
    mfoot    = obj.pose.bones[fk[2]]
    thighi   = obj.pose.bones[ik[0]]
    shini    = obj.pose.bones[ik[1]]
    footi    = obj.pose.bones[ik[2]]
    footroll = obj.pose.bones[ik[3]]
    pole     = obj.pose.bones[ik[4]]
    mfooti   = obj.pose.bones[ik[5]]

    # Stretch
    footi['stretch_length'] = thigh['stretch_length']

    # Clear footroll
    set_pose_rotation(footroll, Matrix())

    # Foot position
    mat = mfooti.bone.matrix_local.inverted() * footi.bone.matrix_local
    footmat = get_pose_matrix_in_other_space(mfoot.matrix, footi) * mat
    set_pose_translation(footi, footmat)
    set_pose_rotation(footi, footmat)
    set_pose_scale(footi, footmat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')

    # Pole target position
    match_pole_target(thighi, shini, pole, thigh, (thighi.length + shini.length))


##############################
## IK/FK snapping operators ##
##############################
def _dokey(step):
    actual = bpy.context.scene.frame_current
    bpy.ops.anim.keyframe_insert()
    actual += step
    bpy.context.scene.frame_set(actual)
    return(actual)
     



class Rigify_Arm_FK2IKEX(bpy.types.Operator):
    """ Snaps an FK arm to an IK arm.
    """
    bl_idname = "pose.rigify_arm_fk2ikex_" + rig_id
    bl_label = "Rigify Snap FK arm to IK"
    bl_options = {'UNDO'}

    uarm_fk = bpy.props.StringProperty(name="Upper Arm FK Name")
    farm_fk = bpy.props.StringProperty(name="Forerm FK Name")
    hand_fk = bpy.props.StringProperty(name="Hand FK Name")

    uarm_ik = bpy.props.StringProperty(name="Upper Arm IK Name")
    farm_ik = bpy.props.StringProperty(name="Forearm IK Name")
    hand_ik = bpy.props.StringProperty(name="Hand IK Name")
    
    start = bpy.props.IntProperty(name="Start")
    end = bpy.props.IntProperty(name="End")
    step = bpy.props.IntProperty(name="Step")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        f = self.start
        bpy.context.scene.frame_set(f)
        while (f < self.end - self.step):
         try:
            fk2ik_arm(context.active_object, fk=[self.uarm_fk, self.farm_fk, self.hand_fk], ik=[self.uarm_ik, self.farm_ik, self.hand_ik])
         finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
         f=_dokey(self.step)
         print("Frame",f)
        return {'FINISHED'}




class Rigify_Leg_FK2IKEX(bpy.types.Operator):
    """ Snaps an FK leg to an IK leg.
    """
    bl_idname = "pose.rigify_leg_fk2ikex_" + rig_id
    bl_label = "Rigify Snap FK leg to IK"
    bl_options = {'UNDO'}

    thigh_fk = bpy.props.StringProperty(name="Thigh FK Name")
    shin_fk  = bpy.props.StringProperty(name="Shin FK Name")
    foot_fk  = bpy.props.StringProperty(name="Foot FK Name")
    mfoot_fk = bpy.props.StringProperty(name="MFoot FK Name")

    thigh_ik = bpy.props.StringProperty(name="Thigh IK Name")
    shin_ik  = bpy.props.StringProperty(name="Shin IK Name")
    foot_ik  = bpy.props.StringProperty(name="Foot IK Name")
    mfoot_ik = bpy.props.StringProperty(name="MFoot IK Name")
    
    start = bpy.props.IntProperty(name="Start")
    end = bpy.props.IntProperty(name="End")
    step = bpy.props.IntProperty(name="Step")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        f = self.start
        bpy.context.scene.frame_set(f)
        while (f < self.end - self.step):
         try:
            fk2ik_leg(context.active_object, fk=[self.thigh_fk, self.shin_fk, self.foot_fk, self.mfoot_fk], ik=[self.thigh_ik, self.shin_ik, self.foot_ik, self.mfoot_ik])
         finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
         _dokey(self.step)
         print("Frame",f)         
        return {'FINISHED'}




###################
## Rig UI Panels ##
###################

class RigUIEX(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Rig FK_Snap_N_Bake"
    bl_idname = rig_id + "_PT_rig_uiex"

    @classmethod
    def poll(self, context):
        if context.mode != 'POSE':
            return False
        try:
            return (context.active_object.data.get("rig_id") == rig_id)
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        pose_bones = context.active_object.pose.bones
        try:
            selected_bones = [bone.name for bone in context.selected_pose_bones]
            selected_bones += [context.active_pose_bone.name]
        except (AttributeError, TypeError):
            return

        def is_selected(names):
            # Returns whether any of the named bones are selected.
            if type(names) == list:
                for name in names:
                    if name in selected_bones:
                        return True
            elif names in selected_bones:
                return True
            return False


        

        
        fk_leg = ["thigh.fk.L", "shin.fk.L", "foot.fk.L", "MCH-foot.L"]
        ik_leg = ["MCH-thigh.ik.L", "MCH-shin.ik.L", "foot.ik.L", "knee_target.ik.L", "foot_roll.ik.L", "MCH-foot.L.001"]
        if is_selected(fk_leg+ik_leg):
            p = layout.operator("pose.rigify_leg_fk2ikex_" + rig_id, text="Snap FK->IK (" + fk_leg[0] + ")")
            p.thigh_fk = fk_leg[0]
            p.shin_fk  = fk_leg[1]
            p.foot_fk  = fk_leg[2]
            p.mfoot_fk = fk_leg[3]
            p.thigh_ik = ik_leg[0]
            p.shin_ik  = ik_leg[1]
            p.foot_ik = ik_leg[2]
            p.mfoot_ik = ik_leg[5]
            p.start = bpy.context.scene.frame_current
            p.end = bpy.context.scene.frame_end
            obj = bpy.context.active_object
            row= layout.row(align=True)
            row.label("start: {0}".format(p.start))
            row.label("end: {0}".format(p.end))
            row.prop(obj, '["%s"]' % ("bakestep"),text="Step")
            p.step = obj["bakestep"]


        
        fk_leg = ["thigh.fk.R", "shin.fk.R", "foot.fk.R", "MCH-foot.R"]
        ik_leg = ["MCH-thigh.ik.R", "MCH-shin.ik.R", "foot.ik.R", "knee_target.ik.R", "foot_roll.ik.R", "MCH-foot.R.001"]
        if is_selected(fk_leg+ik_leg):
            p = layout.operator("pose.rigify_leg_fk2ikex_" + rig_id, text="Snap FK->IK (" + fk_leg[0] + ")")
            p.thigh_fk = fk_leg[0]
            p.shin_fk  = fk_leg[1]
            p.foot_fk  = fk_leg[2]
            p.mfoot_fk = fk_leg[3]
            p.thigh_ik = ik_leg[0]
            p.shin_ik  = ik_leg[1]
            p.foot_ik = ik_leg[2]
            p.mfoot_ik = ik_leg[5]
            p.start = bpy.context.scene.frame_current
            p.end = bpy.context.scene.frame_end
            obj = bpy.context.active_object
            row= layout.row(align=True)
            row.label("start: {0}".format(p.start))
            row.label("end: {0}".format(p.end))
            row.prop(obj, '["%s"]' % ("bakestep"),text="Step")
            p.step = obj["bakestep"]
        

        
        fk_arm = ["upper_arm.fk.L", "forearm.fk.L", "hand.fk.L"]
        ik_arm = ["MCH-upper_arm.ik.L", "MCH-forearm.ik.L", "hand.ik.L", "elbow_target.ik.L"]
        if is_selected(fk_arm+ik_arm):
            p = layout.operator("pose.rigify_arm_fk2ikex_" + rig_id, text="Bake FK from IK (" + fk_arm[0] + ")")
            p.uarm_fk = fk_arm[0]
            p.farm_fk = fk_arm[1]
            p.hand_fk = fk_arm[2]
            p.uarm_ik = ik_arm[0]
            p.farm_ik = ik_arm[1]
            p.hand_ik = ik_arm[2]
            p.start = bpy.context.scene.frame_current
            p.end = bpy.context.scene.frame_end
            obj = bpy.context.active_object
            row= layout.row(align=True)
            row.label("start: {0}".format(p.start))
            row.label("end: {0}".format(p.end))
            row.prop(obj, '["%s"]' % ("bakestep"),text="Step")
            p.step = obj["bakestep"]

        

        
        fk_arm = ["upper_arm.fk.R", "forearm.fk.R", "hand.fk.R"]
        ik_arm = ["MCH-upper_arm.ik.R", "MCH-forearm.ik.R", "hand.ik.R", "elbow_target.ik.R"]
        if is_selected(fk_arm+ik_arm):
            p = layout.operator("pose.rigify_arm_fk2ikex_" + rig_id, text="Snap FK->IK (" + fk_arm[0] + ")")
            p.uarm_fk = fk_arm[0]
            p.farm_fk = fk_arm[1]
            p.hand_fk = fk_arm[2]
            p.uarm_ik = ik_arm[0]
            p.farm_ik = ik_arm[1]
            p.hand_ik = ik_arm[2]
            p.start = bpy.context.scene.frame_current
            p.end = bpy.context.scene.frame_end
            obj = bpy.context.active_object
            row= layout.row(align=True)
            row.label("start: {0}".format(p.start))
            row.label("end: {0}".format(p.end))
            row.prop(obj, '["%s"]' % ("bakestep"),text="Step")
            p.step = obj["bakestep"]

            
     
            


def register():
    bpy.utils.register_class(Rigify_Arm_FK2IKEX)
    bpy.utils.register_class(Rigify_Leg_FK2IKEX)
    bpy.utils.register_class(RigUIEX)

def unregister():
    bpy.utils.unregister_class(Rigify_Arm_FK2IKEX)
    bpy.utils.unregister_class(Rigify_Leg_FK2IKEX)
    bpy.utils.unregister_class(RigUIEX)

register()
