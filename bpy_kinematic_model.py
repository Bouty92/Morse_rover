import bpy
import numpy as np
import math
import mathutils
from math import pi


def new_material( color, backface_culling=True, name='' ) :

	mat = bpy.data.materials.new( name=name )
	mat.diffuse_color = color
	mat.game_settings.use_backface_culling = backface_culling

	return mat


red = new_material( ( 1, 0, 0 ) )
green = new_material( ( 0, 1, 0 ) )
blue = new_material( ( 0, 0, 1 ) )
yellow = new_material( ( 1, 1, 0 ) )
cyan = new_material( ( 0, 1, 1 ) )
orange = new_material( ( 1, 0.2, 0 ) )
magenta = new_material( ( 1, 0, 1 ) )
dark = new_material( ( 0.1, 0.1, 0.1 ) )
steel = new_material( ( 0.4, 0.4, 0.4 ) )
alu = new_material( ( 0.7, 0.7, 0.7 ) )
white = new_material( ( 1, 1, 1 ) )


def join( obj_list ) :

	bpy.ops.object.select_all( action='DESELECT' )
	for obj in obj_list :
		obj.select = True
	bpy.context.scene.objects.active = obj_list[0]
	bpy.ops.object.convert( target='MESH' )
	bpy.ops.object.join()
	

def set_parent( obj_list ) :

	bpy.ops.object.select_all( action='DESELECT' )
	for obj in obj_list :
		obj.select = True
	bpy.context.scene.objects.active = obj_list[0]
	bpy.ops.object.parent_set( type='OBJECT', keep_transform=True )


def vec_to_euler( current_vec, new_vec ) :

	new_vec = new_vec/np.linalg.norm( new_vec )
	current_vec = current_vec/np.linalg.norm( current_vec )
	
	rot_vec = np.cross( current_vec, new_vec )
	if np.linalg.norm( rot_vec ) == 0 :
		if np.dot( current_vec, new_vec ) > 0 :
			return 0, 0, 0
		else :
			rot_vec = np.cross( ( 0, 0, 1 ), new_vec )
			if np.linalg.norm( rot_vec ) == 0 and np.dot( ( 0, 0, 1 ), new_vec ) < 0 :
				return pi, 0, 0

	rot_vec = rot_vec/np.linalg.norm( rot_vec )

	angle = math.acos( np.dot( current_vec, new_vec ) )

	q0 = math.cos( angle/2 )
	q123 = math.sin( angle/2 )*rot_vec
	q1 = q123[0]
	q2 = q123[1]
	q3 = q123[2]

	roll = math.atan2( 2*( q0*q1 + q2*q3 ), 1 - 2*( q1**2 + q2**2 ) )
	pitch = math.asin( 2*( q0*q2 - q3*q1 ) )
	yaw = math.atan2( 2*( q0*q3 + q1*q2 ), 1 - 2*( q2**2 + q3**2 ) )

	return roll, pitch, yaw


def zvec_to_euler( dir_vec ) :

	return vec_to_euler( ( 0, 0, 1 ), dir_vec )


def move_origin( obj, pos ) :

	bpy.context.scene.cursor_location = pos
	bpy.ops.object.origin_set( type='ORIGIN_CURSOR' )


def move_axis( obj, axis, dir_vec ) :

	obj.rotation_euler = vec_to_euler( obj.rotation_euler.to_matrix().inverted()*mathutils.Vector( dir_vec ), axis )
	bpy.ops.object.transform_apply( rotation=True )
	obj.rotation_euler = vec_to_euler( axis, dir_vec )


def track_to( obj, target ) :

	dir_vec = target.location - obj.location

	move_axis( obj, ( 1, 0, 0 ), dir_vec )

	# Render:
	constraint = obj.constraints.new( 'TRACK_TO' )
	constraint.track_axis = 'TRACK_X'
	constraint.up_axis = 'UP_Z'
	constraint.target = target

	# Game:
	bpy.context.scene.objects.active = obj
	bpy.ops.logic.actuator_add( type='CONSTRAINT' )
	obj.game.actuators[-1].type = 'EDIT_OBJECT'
	obj.game.actuators[-1].mode = 'TRACKTO'
	obj.game.actuators[-1].track_axis = 'TRACKAXISX'
	obj.game.actuators[-1].up_axis = 'UPAXISZ'
	obj.game.actuators[-1].use_3d_tracking = True
	obj.game.actuators[-1].track_object = target
	bpy.ops.logic.sensor_add( type='ALWAYS' )
	bpy.ops.logic.controller_add( type='LOGIC_AND' )
	obj.game.sensors[-1].link( obj.game.controllers[-1] )
	obj.game.actuators[-1].link( obj.game.controllers[-1] )


def rod( posA, posB, vecA=None, vecB=None, radius=0.005, bevel_res=1, spline_res=20, mat=None ) :
	
	bpy.ops.curve.primitive_bezier_curve_add( location=( 0, 0, 0 ) )
	obj = bpy.context.object
	obj.data.dimensions = '3D'
	obj.data.fill_mode = 'FULL'
	obj.data.bevel_depth = radius
	obj.data.bevel_resolution = bevel_res
	if vecA is None and vecB is None :
		obj.data.resolution_u = 0
		obj.data.resolution_v = 0
	else :
		obj.data.resolution_u = spline_res
		obj.data.resolution_v = spline_res

	obj.data.splines[0].bezier_points[0].co = posA
	if vecA is None :
		obj.data.splines[0].bezier_points[0].handle_left_type = 'VECTOR'
	else :
		obj.data.splines[0].bezier_points[0].handle_left = np.array( posA ) - np.array( vecA )
		obj.data.splines[0].bezier_points[0].handle_right = np.array( posA ) + np.array( vecA )

	obj.data.splines[0].bezier_points[1].co = posB
	if vecB is None :
		obj.data.splines[0].bezier_points[1].handle_left_type = 'VECTOR'
	else :
		obj.data.splines[0].bezier_points[1].handle_left = np.array( posB ) + np.array( vecB )
		obj.data.splines[0].bezier_points[1].handle_right = np.array( posB ) - np.array( vecB )

	if mat is not None :
		obj.data.materials.append( mat )
	
	return obj


hinge_joint_width = 0.08
hinge_joint_radius = 0.025
hinge_joint_gap = 0.01

def hinge_joint( pos, dir_vec, mat_out=None, mat_in=None ) :

	norm_vec = dir_vec/np.linalg.norm( dir_vec )

	if mat_out is not None :
		mat_out_nobc = mat_out.copy()
		mat_out_nobc.game_settings.use_backface_culling = False

	outer_part = rod( np.array( pos ) - norm_vec*hinge_joint_width/2, np.array( pos ) + norm_vec*hinge_joint_width/2, radius=hinge_joint_radius, bevel_res=4, mat=mat_out_nobc )

	bpy.ops.mesh.primitive_circle_add( location=( np.array( pos ) - norm_vec*( hinge_joint_width/2 + hinge_joint_gap ) ), radius=hinge_joint_radius, fill_type='NGON', vertices=16, rotation=zvec_to_euler( dir_vec ) )
	side_part_1 = bpy.context.object
	bpy.ops.mesh.primitive_circle_add( location=( np.array( pos ) + norm_vec*( hinge_joint_width/2 + hinge_joint_gap ) ), radius=hinge_joint_radius, fill_type='NGON', vertices=16, rotation=zvec_to_euler( dir_vec ) )
	side_part_2 = bpy.context.object

	if mat_in is not None :
		mat_in_nobc = mat_in.copy()
		mat_in_nobc.game_settings.use_backface_culling = False
		side_part_1.data.materials.append( mat_in_nobc )
		side_part_2.data.materials.append( mat_in_nobc )
	
	join( [ outer_part, side_part_1, side_part_2 ] )
	
	return outer_part


def cylinder_ab( posA, posB, radius=0.005, vert=12, smooth=False, mat=None ) :

	center = ( np.array( posA ) + np.array( posB ) )/2
	dir_vec = np.array( posB ) - np.array( posA )
	length = np.linalg.norm( dir_vec )
	bpy.ops.mesh.primitive_cylinder_add( vertices=vert, radius=radius, depth=length, location=center, rotation=zvec_to_euler( dir_vec ) )

	obj = bpy.context.object
	if mat is not None :
		obj.data.materials.append( mat )

	if smooth :
		bpy.ops.object.shade_smooth()
	
	return obj


def cylinder_c( pos, dir_vec, length, radius=0.005, vert=12, smooth=False, mat=None ) :

	bpy.ops.mesh.primitive_cylinder_add( vertices=vert, radius=radius, depth=length, location=pos, rotation=zvec_to_euler( dir_vec ) )

	obj = bpy.context.object
	if mat is not None :
		obj.data.materials.append( mat )

	if smooth :
		bpy.ops.object.shade_smooth()
	
	return obj


def sphere( pos, radius=0.005, segments=8, ring_count=4, mat=None ) :

	#bpy.ops.surface.primitive_nurbs_surface_sphere_add( location=pos, radius=radius )
	bpy.ops.mesh.primitive_uv_sphere_add( location=pos, size=radius, segments=segments, ring_count=ring_count )
	obj = bpy.context.object
	if mat is not None :
		obj.data.materials.append( mat )

	bpy.ops.object.shade_smooth()

	return obj


ball_joint_outer_radius = 0.025
ball_joint_inner_radius = 0.02
ball_joint_cover_offset = 0.005

def ball_joint( pos, dir_vec, mat_out=None, mat_in=None ) :

	outer_part = sphere( pos, ball_joint_outer_radius, 16, 8, mat_out )

	bpy.ops.mesh.primitive_plane_add( radius=2*ball_joint_outer_radius, location=( pos + np.array([ 0, 0, ball_joint_cover_offset ]) ), rotation=( pi, 0, 0 ) )
	plane = bpy.context.object

	bool_op = outer_part.modifiers.new( type="BOOLEAN", name="cut ball" )
	bool_op.object = plane
	bool_op.operation = 'DIFFERENCE'
	#plane.hide = True

	bpy.context.scene.objects.active = outer_part
	res = bpy.ops.object.modifier_apply( modifier = 'cut ball' )

	#bpy.ops.object.select_all( action='DESELECT' )
	plane.select = True
	bpy.ops.object.delete()

	outer_part.rotation_euler = zvec_to_euler( dir_vec )

	inner_part = sphere( pos, ball_joint_inner_radius, 16, 8, mat_in )

	join( [ outer_part, inner_part ] )

	return outer_part


def rod_suite( pos_list, radius=0.005, mat=None ) :

	obj_list = []

	for i in range( 1, len( pos_list ) - 1 ) :
		obj_list.append( rod( pos_list[i-1], pos_list[i], radius=radius, mat=mat ) )
		obj_list.append( sphere( pos_list[i], radius, mat=mat ) )

	obj_list.append( rod( pos_list[-2], pos_list[-1], radius=radius, mat=mat ) )

	join( obj_list )

	return obj_list[0]


def spring( posA, posB, widthA=0.02, widthB=0.02, radius=0.002, gap=0.004, resolution=100, mat=None ) :

	vec = np.array( posB ) - np.array( posA )
	length = np.linalg.norm( vec )
	step = length/( resolution - 1 )
	omega = 2*pi/( 2*radius + gap )*step

	# Sample data:
	coords = []
	for i in range( resolution ) :
		width = widthA + ( widthB - widthA )/( resolution - 1 )*i
		coords.append( np.array([ width*math.cos( omega*i ), width*math.sin( omega*i ), step*i ]) )

	# Create the Curve Datablock:
	curveData = bpy.data.curves.new( 'myCurve', type='CURVE' )
	curveData.dimensions = '3D'
	#curveData.resolution_u = 2

	# Map coords to spline:
	polyline = curveData.splines.new( 'NURBS' )
	polyline.points.add( len( coords ) )
	for i, coord in enumerate( coords ):
		x, y, z = coord
		polyline.points[i].co = ( x, y, z, 1 )

	# Create object:
	spiral = bpy.data.objects.new( 'myCurve', curveData )
	spiral.location = posA

	# Attach to scene and validate context:
	scn = bpy.context.scene
	scn.objects.link( spiral )
	scn.objects.active = spiral
	spiral.select = True

	spiral.data.splines[0].use_endpoint_u = True
	spiral.data.fill_mode = 'FULL'
	spiral.data.bevel_depth = radius
	spiral.data.bevel_resolution = 1
	spiral.data.resolution_u = 0

	spiral.rotation_euler = zvec_to_euler( vec )
	if mat is not None :
		spiral.data.materials.append( mat )

	norm_vec = vec/np.linalg.norm( vec )

	rot_vec = np.cross( ( 0, 0, 1 ), norm_vec )
	if np.linalg.norm( rot_vec ) == 0 :
		if np.dot( ( 0, 0, 1 ), norm_vec ) > 0 :
			angle = 0
		else :
			angle = pi
		rot_vec = np.array([ 1, 0, 0 ])
	else :
		rot_vec = rot_vec/np.linalg.norm( rot_vec )
		angle = math.acos( np.dot( ( 0, 0, 1 ), norm_vec ) )

	a = math.cos( angle/2 )
	bcd = math.sin( angle/2 )*rot_vec
	b = bcd[0]
	c = bcd[1]
	d = bcd[2]

	rot_matrix = np.array([ [ a**2 + b**2 - c**2 - d**2, 2*b*c - 2*a*d, 2*a*c + 2*b*d ], \
	[ 2*a*d + 2*b*c, a**2 - b**2 + c**2 - d**2, 2*c*d - 2*a*b ], \
	[ 2*b*d - 2*a*c, 2*a*b + 2*c*d, a**2 - b**2 - c**2 + d**2 ]])

	coA = np.dot( rot_matrix, coords[0] ) + posA
	coB = np.dot( rot_matrix, coords[-1] ) + posA

	obj_list = [ spiral ]

	obj_list.append( sphere( coA, radius, mat=mat ) )
	obj_list.append( sphere( coB, radius, mat=mat ) )
	obj_list.append( rod( coA, posA, radius=radius, mat=mat ) )
	obj_list.append( rod( coB, posB, radius=radius, mat=mat ) )
	obj_list.append( sphere( posA, radius, mat=mat ) )
	obj_list.append( sphere( posB, radius, mat=mat ) )

	join( obj_list )

	return spiral


def linked_spring( posA, posB, parentA=None, parentB=None, widthA=0.02, widthB=0.02, radius=0.002, gap=0.004, resolution=100, mat=None ) :

	spr = spring( posA, posB, widthA, widthB, radius, gap, resolution, mat )

	frame_size = 0.02

	bpy.ops.object.empty_add( type='SPHERE', location=posA )
	frame1 = bpy.context.object
	frame1.scale = ( frame_size, frame_size, frame_size )
	if parentA is not None :
		set_parent( [ parentA, frame1 ] )

	bpy.ops.object.empty_add( type='SPHERE', location=posB )
	frame2 = bpy.context.object
	frame2.scale = ( frame_size, frame_size, frame_size )
	if parentB is not None :
		set_parent( [ parentB, frame2 ] )

	bpy.ops.object.armature_add( location=( 0, 0, 0 ) )
	armature = bpy.context.object
	armature.draw_type = 'WIRE'
	armature.show_x_ray = True

	bpy.ops.object.mode_set( mode='EDIT' )

	eb = armature.data.edit_bones[0]
	eb.head = posA
	eb.tail = posB

	bpy.ops.object.mode_set( mode='OBJECT' )

	set_parent( [ frame1, armature ] )
	
	constraint = armature.pose.bones[-1].constraints.new( 'STRETCH_TO' )
	constraint.target = frame2
	constraint.volume = 'NO_VOLUME'
	constraint.keep_axis = 'PLANE_Z'

	bpy.context.scene.objects.active = armature
	bpy.ops.logic.actuator_add( type='ARMATURE' )
	bpy.ops.logic.sensor_add( type='ALWAYS' )
	bpy.ops.logic.controller_add( type='LOGIC_AND' )
	armature.game.sensors[-1].link( armature.game.controllers[-1] )
	armature.game.actuators[-1].link( armature.game.controllers[-1] )

	bpy.ops.object.select_all( action='DESELECT' )
	spr.select = True
	armature.select = True
	bpy.context.scene.objects.active = armature
	bpy.ops.object.parent_set( type='ARMATURE_AUTO', keep_transform=True )

	return frame1, frame2, armature, spr


def linear_actuator( posA, posB, parentA=None, parentB=None, cylinder_length=0.15, cylinder_radius=0.02, cylinder_vert=12, rod_radius=0.005, matA=None, matB=None, cylinder_mat=dark, rod_mat=alu ) :

	vec = np.array( posB ) - np.array( posA )
	vec = vec/np.linalg.norm( vec )

	obj_ball_cylinder = ball_joint( posA, vec, matA, cylinder_mat )
	if parentA is not None :
		set_parent( [ parentA, obj_ball_cylinder ] )

	obj_ball_rod = ball_joint( posB, -vec, matB, rod_mat )
	if parentB is not None :
		set_parent( [ parentB, obj_ball_rod ] )

	gap = ball_joint_inner_radius - math.sqrt( ball_joint_inner_radius**2 - rod_radius**2 )
	obj_cylinder = cylinder_ab( posA + ( ball_joint_inner_radius - gap )*vec, np.array( posA ) + cylinder_length*vec, cylinder_radius, cylinder_vert, mat=cylinder_mat )
	move_origin( obj_cylinder, posA )
	set_parent( [ obj_ball_cylinder, obj_cylinder ] )
	track_to( obj_cylinder, obj_ball_rod )

	obj_rod = rod( posA + ( ball_joint_inner_radius - gap + cylinder_length/2 )*vec, posB, mat=rod_mat )
	move_origin( obj_rod, posB )
	set_parent( [ obj_ball_rod, obj_rod ] )
	track_to( obj_rod, obj_ball_cylinder )
	join( [ obj_rod ] )

	return obj_ball_cylinder, obj_ball_rod, obj_cylinder, obj_rod


def body_model( pos, mass, size, rot=( 0, 0, 0 ), children=None, name=None ) :

	bpy.ops.mesh.primitive_cube_add( radius=1, location=pos, rotation=rot )
	obj = bpy.context.object
	obj.scale = ( size[0]/2, size[1]/2, size[2]/2 )
	bpy.ops.object.transform_apply( location=False, rotation=False, scale=True )
	obj.draw_type = 'WIRE'
	obj.game.physics_type = 'RIGID_BODY'
	obj.game.use_ghost = True
	obj.hide_render = True
	obj.game.mass = mass

	if name is not None :
		obj.name = name

	if children is not None :
		try :
			iter( children )
		except :
			children = [ children ]

		set_parent( [ obj ] + children )

		for child in children :
			child.game.physics_type = 'NO_COLLISION'

	return obj


def add_hinge_joint( owner, target, pos, dir_vec, limits=None, linked_collision=False, name=None ) :

	constraint = owner.constraints.new( 'RIGID_BODY_JOINT' )
	constraint.target = target
	constraint.use_linked_collision = linked_collision
	constraint.pivot_type = 'HINGE'
	constraint.show_pivot = True

	mat = owner.rotation_euler.to_matrix().inverted()

	pos = mat*( mathutils.Vector( pos ) - mathutils.Vector( owner.location ) )
	constraint.pivot_x = pos[0]
	constraint.pivot_y = pos[1]
	constraint.pivot_z = pos[2]

	local_vec = mat*mathutils.Vector( dir_vec )
	rot = vec_to_euler( ( 1, 0, 0 ), local_vec )
	constraint.axis_x = rot[0]
	constraint.axis_y = rot[1]
	constraint.axis_z = rot[2]

	if limits is not None :
		constraint.use_angular_limit_x = True
		constraint.limit_angle_min_x = limits[0]
		constraint.limit_angle_max_x = limits[1]

	if name is not None :
		constraint.name = name

	return constraint


class kinematics_armature :

	bones_size = 0.2

	def __init__( self, name, head, tail, child=None ) :

		bpy.ops.object.armature_add( location=( 0, 0, 0 ) )
		self._armature = bpy.context.object
		self._armature.draw_type = 'WIRE'
		self._armature.show_x_ray = True

		bpy.ops.object.mode_set( mode='EDIT' )

		eb = self._armature.data.edit_bones[0]
		eb.name = name
		eb.head = head
		eb.tail = tail

		self._armature.data.edit_bones.active = self._armature.data.edit_bones[name]

		bpy.ops.object.mode_set( mode='OBJECT' )

		if child is not None :
			bpy.ops.object.select_all( action='DESELECT' )
			child.select = True
			self._armature.select = True
			bpy.context.scene.objects.active = self._armature
			bpy.ops.object.parent_set( type='BONE', keep_transform=True )
	
	def add_hinge_joint( self, name, pos, dir_vec, child=None, parent=None, limits=None ) :

		bpy.ops.object.mode_set( mode='EDIT' )

		eb = self._armature.data.edit_bones.new( name )

		if parent is not None :
			eb.parent = self._armature.data.edit_bones[parent]

		eb.head = pos

		dir_vec = dir_vec/np.linalg.norm( dir_vec )
		vec = np.cross( dir_vec, np.array([ 1, 0, 0 ]) )
		if np.linalg.norm( vec ) == 0 :
			vec = np.array([ 0, 1, 0 ])

		eb.tail = pos + self.bones_size*vec

		eb.roll -= math.acos( np.dot( dir_vec, eb.x_axis ) )

		self._armature.data.edit_bones.active = self._armature.data.edit_bones[name]

		bpy.ops.object.mode_set( mode='OBJECT' )

		if child is not None :
			bpy.ops.object.select_all( action='DESELECT' )
			child.select = True
			self._armature.select = True
			bpy.context.scene.objects.active = self._armature
			bpy.ops.object.parent_set( type='BONE', keep_transform=True )
		
		constraint = self._armature.pose.bones.get( name ).constraints.new( 'IK' )
		constraint.name = 'hinge ' + name
		constraint.chain_count = 1
		bone = bpy.context.object.pose.bones[name]
		bone.lock_ik_y = True
		bone.lock_ik_z = True
		if limits is not None :
			bone.use_ik_limit_x = True
			bone.ik_min_x = limits[0]
			bone.ik_max_x = limits[1]


#from mathutils import Vector

#def triangles (verts):
	#"""enumerate triangles in a face"""
	#for i in range (1, len(verts)-1):
		#yield (verts[0], verts[i], verts[i+1])

#def cg_mesh (obj):
	#"""center of mass (and volume) of a mesh"""

	#center = Vector()
	#volume = 0
	#mesh = obj.to_mesh (bpy.context.scene, True, 'PREVIEW')
	#for face in mesh.polygons:
		#f = face.vertices
		#for t in triangles (f):
			#a,b,c = (mesh.vertices[v].co for v in t)
			#v = a.cross(b).dot(c) / 6
			#center += v * (a+b+c) / 4
			#volume += v
	#bpy.data.meshes.remove(mesh)

	#if volume == 0: print ("ZERO VOLUME", obj.name)
	#else          : center /= volume

	#return obj.matrix_world * center

## puts the cursor at the active object's center of mass
#bpy.context.scene.cursor_location = cg_mesh (bpy.context.scene.objects.active)


if __name__ == '__main__' :

	if bpy.ops.object.mode_set.poll() :
		bpy.ops.object.mode_set( mode='OBJECT' )
	bpy.ops.object.select_all( action='SELECT' )
	bpy.ops.object.delete()

	posA = ( 0.1, 0.1, 0.1 )
	posB = posA + 0.1*np.array([ 0, 1, 1 ])

	rod1 = rod( posA - np.array([ 0.1, 0, 0 ]), posA, mat=red )
	rod2 = rod( posB - np.array([ 0.1, 0, 0 ]), posB, mat=blue )
	join( [ rod1 ] )
	join( [ rod2 ] )

	#move_origin( rod1, posA )
	#move_origin( rod2, posB )

	rod1_BM = body_model( posA - np.array([ 0.1, 0, 0 ])/2, 0.5, ( 0.1, 0.01, 0.01 ), children=rod1 )
	rod2_BM = body_model( posB - np.array([ 0.1, 0, 0 ])/2, 0.5, ( 0.1, 0.01, 0.01 ), children=rod2 )

	#actu = linear_actuator( posA, posB, rod1, rod2, matA=red, matB=blue )

	linked_spring( posA, posB, rod1, rod2 )


	bpy.ops.object.select_all( action='DESELECT' )
