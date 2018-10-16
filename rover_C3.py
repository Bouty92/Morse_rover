from bpy_kinematic_model import *

if __name__ == '__main__' :
	if bpy.ops.object.mode_set.poll() :
		bpy.ops.object.mode_set( mode='OBJECT' )
	bpy.ops.object.select_all( action='SELECT' )
	bpy.ops.object.delete()


##############
# PARAMETERS #
##############

wheelbase = 0.7
track = 0.7
wheels_radius = 0.15
wheels_width = 0.1
wheels_vertices = 80
wheels_color = dark
wheels_axle_y = track/2 - 0.08
wheels_mass = 2

torque_sensor_height = wheels_radius + 0.05
axles_BM_size = ( torque_sensor_height - wheels_radius, track/2 - wheels_axle_y, torque_sensor_height - wheels_radius )
axles_BM_mass = 0.1

chassis_height = 0.3

steering_limit = 50
boggie_limit = 50
sea_hinge_limit = 40

boggie_height = 0.3
boggie_x = -0.2

sea_hinge_gap_x = 0.06
sea_hinge_gap_z = 0.07
#sea_hinge_x = -wheelbase/2 + 2
sea_hinge_x = boggie_x - hinge_joint_width - 2*hinge_joint_gap

s_actuator_pos1 = ( 0.28, -0.1, chassis_height )
s_actuator_pos2 = ( -0.1, -0.16, chassis_height )
s_actuator_length = 0.22

r_actuator_gap = 0.07
r_actuator_pos1 = ( -0.1, 0.2, chassis_height + 0.1 )
r_actuator_pos2 = ( -0.1, -0.06, chassis_height + 0.1 )
r_actuator_length = 0.16

spring_pos1 = ( boggie_x - 0.015, r_actuator_pos2[1], r_actuator_pos2[2] )
spring_pos2 = ( boggie_x - 0.015, r_actuator_pos2[1] - 0.06, chassis_height )
spring_width = 0.01
spring_gap = 0.007
spring_color = alu

front_frame_color = red
front_frame_BM_CoM = ( wheelbase/4, 0, chassis_height + 0.05 )
front_frame_BM_size = ( wheelbase/2, 0.3, 0.2 )
front_frame_BM_mass = 5

rear_frame_color = blue
rear_frame_BM_CoM = ( ( sea_hinge_x - hinge_joint_width/2 - hinge_joint_gap )/2, 0, chassis_height + 0.05 )
rear_frame_BM_size = ( ( sea_hinge_x - hinge_joint_width/2 - hinge_joint_gap ), 0.3, 0.2 )
rear_frame_BM_mass = 1

boggie_color = green
boggie_BM_CoM = ( ( boggie_x - wheelbase/2 )/2, 0, ( torque_sensor_height + chassis_height )/2 )
boggie_BM_size = ( abs( -wheelbase/2 - boggie_x ), wheels_axle_y*2, chassis_height - torque_sensor_height )
boggie_BM_mass = 2

sea_hinge_color = cyan
sea_hinge_BM_CoM = ( ( sea_hinge_x + r_actuator_pos2[0] )/2, r_actuator_pos2[1]/2, ( chassis_height + r_actuator_pos2[2] )/2 )
sea_hinge_BM_size = ( abs( r_actuator_pos2[0] - sea_hinge_x ), abs( r_actuator_pos2[1] ), r_actuator_pos2[2] - chassis_height )
sea_hinge_BM_mass = 2


###########
# DISPLAY #
###########

# Wheels:
wheels = []
for i in range( 4 ) :
	wheels.append( cylinder_c( ( ( -1 if i//2 else 1 )*wheelbase/2, ( -1 if i%2 else 1 )*track/2, wheels_radius ), ( 0, 1, 0 ), wheels_width, wheels_radius, wheels_vertices, mat=wheels_color ) )
	wheels[i].name = 'wheel ' + str( i + 1 )

for i in range( 4 ) :
	marker = cylinder_c( ( ( -1 if i//2 else 1 )*wheelbase/2, ( -1 if i%2 else 1 )*track/2, wheels_radius/3 ), ( 0, 1, 0 ), wheels_width + 0.001, wheels_radius/6, 4, mat=white )
	marker.game.physics_type = 'NO_COLLISION'
	set_parent( [ wheels[i], marker ] )

# Wheel axles:
axles = []
for i in range( 4 ) :
	axles.append( rod_suite( [ ( ( -1 if i//2 else 1 )*wheelbase/2, ( -1 if i%2 else 1 )*track/2, wheels_radius ), \
	                           ( ( -1 if i//2 else 1 )*wheelbase/2, ( -1 if i%2 else 1 )*wheels_axle_y, wheels_radius ), \
							   ( ( -1 if i//2 else 1 )*wheelbase/2, ( -1 if i%2 else 1 )*wheels_axle_y, torque_sensor_height ) ], mat=yellow ) )

# Front frame:
front_frame = [ rod_suite( [ ( wheelbase/2, 0, chassis_height ), ( sea_hinge_gap_x, 0, chassis_height ), ( sea_hinge_gap_x, 0, chassis_height + sea_hinge_gap_z ), \
( 0, 0, chassis_height + sea_hinge_gap_z ), ( 0, 0, chassis_height - hinge_joint_width/2 - hinge_joint_gap ) ], mat=front_frame_color ) ]
front_frame.append( sphere( ( wheelbase/2, wheels_axle_y, torque_sensor_height ), mat=front_frame_color ) )
front_frame.append( sphere( ( wheelbase/2, -wheels_axle_y, torque_sensor_height ), mat=front_frame_color ) )
front_frame.append( rod( ( wheelbase/2, wheels_axle_y, torque_sensor_height ), ( wheelbase/2, 0, chassis_height ), ( 0, 0, 0 ), ( 0, track/2.5, 0 ), mat=front_frame_color ) )
front_frame.append( rod( ( wheelbase/2, -wheels_axle_y, torque_sensor_height ), ( wheelbase/2, 0, chassis_height ), ( 0, 0, 0 ), ( 0, -track/2.5, 0 ), mat=front_frame_color ) )

# Rear frame:
rear_frame = [ hinge_joint( ( 0, 0, chassis_height ), ( 0, 0, 1 ), rear_frame_color, front_frame_color ) ]
rear_frame.append( rod( ( 0, 0, chassis_height ), ( sea_hinge_x - hinge_joint_width/2 - hinge_joint_gap, 0, chassis_height ), mat=rear_frame_color ) )

# Boggie:
boggie = [ hinge_joint( ( boggie_x, 0, chassis_height ), ( 1, 0, 0 ), boggie_color, rear_frame_color ) ]
boggie.append( sphere( ( -wheelbase/2, wheels_axle_y, torque_sensor_height ), mat=boggie_color ) )
boggie.append( sphere( ( -wheelbase/2, -wheels_axle_y, torque_sensor_height ), mat=boggie_color ) )
boggie.append( rod( ( -wheelbase/2, wheels_axle_y, torque_sensor_height ), ( boggie_x, 0, chassis_height ), ( 0, 0, 0.1 ), ( 0, track/3, 0 ), mat=boggie_color ) )
boggie.append( rod( ( -wheelbase/2, -wheels_axle_y, torque_sensor_height ), ( boggie_x, 0, chassis_height ), ( 0, 0, 0.1 ), ( 0, -track/3, 0 ), mat=boggie_color ) )

# SEA hinge:
sea_hinge = [ hinge_joint( ( sea_hinge_x, 0, chassis_height ), ( 1, 0, 0 ), sea_hinge_color, rear_frame_color ) ]
sea_hinge.append( rod_suite( [ ( sea_hinge_x, 0, chassis_height ), ( sea_hinge_x, r_actuator_pos2[1], r_actuator_pos2[2] ), r_actuator_pos2 ], mat=sea_hinge_color ) )

# Steering actuator:
front_frame.append( rod( ( s_actuator_pos1[0], 0, chassis_height ), s_actuator_pos1, mat=front_frame_color ) )
rear_frame.append( rod( ( s_actuator_pos2[0], 0, chassis_height ), s_actuator_pos2, mat=rear_frame_color ) )
s_actuator = linear_actuator( s_actuator_pos1, s_actuator_pos2, front_frame[0], rear_frame[0], s_actuator_length, matA=front_frame_color, matB=rear_frame_color )

# Roll actuator:
rear_frame.append( rod_suite( [ ( r_actuator_pos1[0], 0, chassis_height ), ( r_actuator_pos1[0], r_actuator_pos1[1], chassis_height ), r_actuator_pos1 ], mat=rear_frame_color ) )
r_actuator = linear_actuator( r_actuator_pos1, r_actuator_pos2, rear_frame[0], sea_hinge[0], r_actuator_length, matA=rear_frame_color, matB=sea_hinge_color )

# Spring:
linked_spring( spring_pos1, spring_pos2, sea_hinge[0], boggie[0], spring_width, spring_width, gap=spring_gap, mat=spring_color, resolution=100 )
#sea_hinge.append( ball_joint( spring_pos1, np.array( spring_pos2 ) - np.array( spring_pos1 ), sea_hinge_color, spring_color ) )
#boggie.append( ball_joint( spring_pos2, np.array( spring_pos1 ) - np.array( spring_pos2 ), boggie_color, spring_color ) )

join( front_frame )
join( rear_frame )
join( boggie )
join( sea_hinge )


#################
# DYNAMIC MODEL #
#################

front_frame_BM = body_model( front_frame_BM_CoM, front_frame_BM_mass, front_frame_BM_size, children=front_frame[0], name='front frame' )
rear_frame_BM = body_model( rear_frame_BM_CoM, rear_frame_BM_mass, rear_frame_BM_size, children=rear_frame[0], name='rear frame' )
boggie_BM = body_model( boggie_BM_CoM, boggie_BM_mass, boggie_BM_size, children=boggie[0], name='boggie' )
sea_hinge_BM = body_model( sea_hinge_BM_CoM, sea_hinge_BM_mass, sea_hinge_BM_size, children=sea_hinge[0], name='sea hinge' )

add_hinge_joint( front_frame_BM, rear_frame_BM, ( 0, 0, chassis_height ), ( 0, 0, 1 ), name='steering joint', limits=[ -steering_limit*pi/180, steering_limit*pi/180 ] )
add_hinge_joint( rear_frame_BM, boggie_BM, ( boggie_x, 0, chassis_height ), ( 1, 0, 0 ), name='boggie joint', limits=[ -boggie_limit*pi/180, boggie_limit*pi/180 ] )
add_hinge_joint( sea_hinge_BM, rear_frame_BM, ( sea_hinge_x, 0, chassis_height ), ( 1, 0, 0 ), name='sea joint', limits=[ -sea_hinge_limit*pi/180, sea_hinge_limit*pi/180 ] )

axles_BM = []
for i in range( 4 ) :
	axles_BM.append( body_model( ( ( -1 if i//2 else 1 )*wheelbase/2, ( -1 if i%2 else 1 )*( track/2 + wheels_axle_y )/2, wheels_radius ), \
	                             axles_BM_mass, axles_BM_size, children=axles[i], name='axles ' + str( i + 1 ) ) )

for i in range( 4 ) :
	add_hinge_joint( wheels[i], axles_BM[i], ( ( -1 if i//2 else 1 )*wheelbase/2, ( -1 if i%2 else 1 )*track/2, wheels_radius ), ( 0, 1, 0 ), name='wheel ' + str( i + 1 ) )
	add_hinge_joint( axles_BM[i], front_frame_BM if i < 2 else boggie_BM, \
	                 ( ( -1 if i//2 else 1 )*wheelbase/2, ( -1 if i%2 else 1 )*wheels_axle_y, torque_sensor_height ), ( 0, 1, 0 ), name='leg ' + str( i ) )


##################
# BOUNDING BOXES #
##################

for wheel in wheels :
	wheel.game.physics_type = 'RIGID_BODY'
	wheel.game.use_collision_bounds = True
	wheel.game.collision_bounds_type = 'CYLINDER'
	wheel.game.mass = wheels_mass


if __name__ == '__main__' :

	############
	# ARMATURE #
	############

	kine = kinematics_armature( 'front frame', ( wheelbase/2, 0, chassis_height ), ( 0, 0, chassis_height ), front_frame[0] )
	kine.add_hinge_joint( 'rear frame', ( 0, 0, chassis_height ), ( 0, 0, 1 ), rear_frame[0], 'front frame', [ -steering_limit*pi/180, steering_limit*pi/180 ] )
	kine.add_hinge_joint( 'boggie', ( boggie_x, 0, chassis_height ), ( 1, 0, 0 ), boggie[0], 'rear frame', [ -boggie_limit*pi/180, boggie_limit*pi/180 ] )
	kine.add_hinge_joint( 'sea hinge', ( sea_hinge_x, 0, chassis_height ), ( 1, 0, 0 ), sea_hinge[0], 'rear frame', [ -sea_hinge_limit*pi/180, sea_hinge_limit*pi/180 ] )
	kine.add_hinge_joint( 'wheel 1', ( wheelbase/2, track/2, wheels_radius ), ( 0, 1, 0 ), wheels[0], 'front frame' )
	kine.add_hinge_joint( 'wheel 2', ( wheelbase/2, -track/2, wheels_radius ), ( 0, 1, 0 ), wheels[1], 'front frame' )
	kine.add_hinge_joint( 'wheel 3', ( -wheelbase/2, track/2, wheels_radius ), ( 0, 1, 0 ), wheels[2], 'boggie' )
	kine.add_hinge_joint( 'wheel 4', ( -wheelbase/2, -track/2, wheels_radius ), ( 0, 1, 0 ), wheels[3], 'boggie' )


	bpy.ops.object.select_all( action='DESELECT' )
