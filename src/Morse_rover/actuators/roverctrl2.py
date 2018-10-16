import logging; logger = logging.getLogger( "morse." + __name__ )

import morse.core.actuator

from morse.core.services import service, async_service, interruptible
from morse.core import status
from morse.helpers.components import add_data, add_property
from morse.core import blenderapi

import bpy
from mathutils import Vector
from math import pi, copysign, tan


class hingeController() :

	def __init__( self, obj1, obj2, dir_vec, mode='ANGLE', Kp=0, Ki=0, Kd=0, max_torque=None, angle0=0 ) :

		self.obj1 = obj1
		self.obj2 = obj2

		world_dir_vec = Vector( dir_vec ).normalized()
		self.local_dir_vec1 = obj1.worldOrientation.inverted()*world_dir_vec
		self.local_dir_vec2 = obj2.worldOrientation.inverted()*world_dir_vec

		world_ang_vec = world_dir_vec.cross( ( 0, 0, 1 ) )
		if world_ang_vec.dot( world_ang_vec ) == 0 :
			world_ang_vec = Vector(( 1, 0, 0 ))
		else :
			world_ang_vec.normalize()
		self.local_ang_vec1 = obj1.worldOrientation.inverted()*world_ang_vec
		self.local_ang_vec2 = obj2.worldOrientation.inverted()*world_ang_vec

		self.mode = mode
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd
		self.max_torque = max_torque
		self.angle0 = angle0
		self.value = 0
		self.int_err = 0
		self.prev_err = 0
		self.prev_time = blenderapi.persistantstorage().time.time

	def getAngle( self ) :
		
		world_ang_vec1 = self.obj1.worldOrientation*self.local_ang_vec1
		world_ang_vec2 = self.obj2.worldOrientation*self.local_ang_vec2

		world_dir_vec = ( self.obj1.worldOrientation*self.local_dir_vec1 + self.obj2.worldOrientation*self.local_dir_vec2 )/2

		return copysign( world_ang_vec1.angle( world_ang_vec2 ), world_ang_vec2.cross( world_ang_vec1 ).dot( world_dir_vec ) ) + self.angle0

	def getAngleRate( self ) :
		
		vel1 = self.obj1.getAngularVelocity( True ).dot( self.local_dir_vec1 )
		vel2 = self.obj2.getAngularVelocity( True ).dot( self.local_dir_vec2 )

		return vel1 - vel2

	def applyTorque( self, torque ) :

		self.obj1.applyTorque( self.local_dir_vec1*torque, True )
		self.obj2.applyTorque( -self.local_dir_vec2*torque, True )

	def update( self, value=None ) :
		
		if value is not None :
			self.value = value

		true_value = self.getAngleRate() if self.mode == 'SPEED' else self.getAngle()

		err = value - true_value

		time = blenderapi.persistantstorage().time.time
		elapsed_time = time - self.prev_time

		self.int_err += ( self.prev_err + err )/2*elapsed_time

		torque = self.Kp*err + self.Ki*self.int_err
		if elapsed_time > 0 :
			torque += self.Kd*( err - self.prev_err )/elapsed_time

		if self.max_torque is not None :
			torque = min( self.max_torque, max( -self.max_torque, torque ) )

		self.applyTorque( torque )

		self.prev_err = err
		self.prev_time = time

		return true_value, torque


class Roverctrl2( morse.core.actuator.Actuator ) :
	"""Write here the general documentation of your actuator.
	It will appear in the generated online documentation.
	"""
	_name = "Roverctrl2"
	_short_desc = "Management of the rover actuation"

	# define here the data fields required by your actuator
	# format is: field name, initial value, type, description
	add_data( 'speed', 0, 'float', 'Desired speed of the rover' )
	add_data( 'angle', 0, 'float', 'Desired steering angle of the rover' )
	add_data( 'torque', 0, 'float', 'Torque to be applied on the boggie of the rover' )
	add_data( 'crawl', False, 'bool', 'Crawling mode for wheel speed' )


	def __init__( self, obj, parent=None ):
		logger.info( "%s initialization" % obj.name )
		# Call the constructor of the parent class
		morse.core.actuator.Actuator.__init__( self, obj, parent )

		self.scene = parent.bge_object.scene

		#for obj in self.scene.objects :
			#print( obj.name )

		self.wheels_radius = 0.15
		self.wheelbase = 0.7
		self.track = 0.7

		self.sea_stiffness = 200
		#self.sea_Kp = 0
		#self.sea_Ki = 0
		#self.sea_Kd = 0
		self.sea_angle_limit = 40*pi/180

		self.front_frame = self.scene.objects['front frame']
		self.rear_frame = self.scene.objects['rear frame']
		self.boggie = self.scene.objects['boggie']
		self.sea_hinge = self.scene.objects['sea hinge']
		self.wheels = []
		for i in range( 4 ) :
			self.wheels.append( self.scene.objects['wheel ' + str( i + 1 )] )
		self.axles = []
		for i in range( 4 ) :
			self.axles.append( self.scene.objects['axles ' + str( i + 1 )] )

		self.wheels_Kp = 1.2
		self.wheels_Ki = 0
		self.wheels_Kd = 0
		self.wheels_max_torque = 10
		self.wheels_controllers = []
		for i in range( 4 ) :
			self.wheels_controllers.append( hingeController( self.wheels[i], self.axles[i], ( 0, 1, 0 ), 'SPEED', self.wheels_Kp, self.wheels_Ki, self.wheels_Kd, self.wheels_max_torque ) )

		self.steering_Kp = 200
		self.steering_Ki = 10
		self.steering_Kd = 50
		self.steering_max_torque = 100
		self.steering_controller = hingeController( self.rear_frame, self.front_frame, ( 0, 0, 1 ), Kp=self.steering_Kp, Ki=self.steering_Ki, Kd=self.steering_Kd, max_torque=self.steering_max_torque )
		
		self.sea_hinge_Kp = 200
		self.sea_hinge_Ki = 10
		self.sea_hinge_Kd = 50
		self.sea_hinge_max_torque = 100
		#self.sea_hinge_controller = hingeController( self.sea_hinge, self.rear_frame, ( 1, 0, 0 ), 'SPEED', Kp=self.sea_hinge_Kp, Ki=self.sea_hinge_Ki, Kd=self.sea_hinge_Kd, max_torque=self.sea_hinge_max_torque )
		self.sea_hinge_controller = hingeController( self.sea_hinge, self.rear_frame, ( 1, 0, 0 ), Kp=self.sea_hinge_Kp, Ki=self.sea_hinge_Ki, Kd=self.sea_hinge_Kd, max_torque=self.sea_hinge_max_torque )
		self.sea_spring = hingeController( self.sea_hinge, self.boggie, ( 1, 0, 0 ) )

		self.leg_stiffness = 200
		self.torque_sensors = []
		for i in range( 4 ) :
			self.torque_sensors.append( hingeController( self.axles[i], ( self.front_frame if i < 2 else self.boggie ), ( 0, 1, 0 ) ) )

		logger.info( 'Component initialized' )

	@service
	def get_counter( self ):
		""" This is a sample service.

		Simply returns the value of the internal counter.

		You can access it as a RPC service from clients.
		"""
		#logger.info( "%s counter is %s" % ( self.name, self.local_data['counter'] ) )

		#return self.local_data['counter']

	@interruptible
	@async_service
	def async_test( self, value ):
		""" This is a sample asynchronous service.

		Returns when the internal counter reaches ``value``.

		You can access it as a RPC service from clients.
		"""
		#self._target_count = value

	def default_action( self ):
		""" Main loop of the actuator.

		Implements the component behaviour
		"""

		# Wheel speed control:
		robot_speed = self.local_data['speed']

		beta = self.steering_controller.getAngle()
		dbeta_dt = self.steering_controller.getAngleRate()

		if self.local_data['crawl'] :
			diff = []
			trans = []
			min_speed = 0
			for i, controller in enumerate( self.wheels_controllers ) :
				diff.append( ( -1 if i%2 else 1 )*self.track/self.wheelbase*tan( beta/2 ) )
				trans.append( ( -1 if i//2 else 1 )*( -self.wheelbase*tan( beta/2 ) + ( -1 if i%2 else 1 )*self.track )*dbeta_dt )
				min_speed = max( min_speed, -trans[i]/( 1 + diff[i] ) )
			robot_speed += min_speed
			for i, controller in enumerate( self.wheels_controllers ) :
				true_speed, torque = controller.update( ( robot_speed*( 1 + diff[i] ) + trans[i] )/self.wheels_radius )
				#print( ( robot_speed*( 1 + diff[i] ) + trans[i] )/self.wheels_radius, end=' ' )
			#print( '\n' )
		else :
			for i, controller in enumerate( self.wheels_controllers ) :
				omega_steer = ( -1 if i//2 else 1 )*( -self.wheelbase*tan( beta/2 ) + ( -1 if i%2 else 1 )*self.track )*dbeta_dt/self.wheels_radius
				omega_turn = ( -1 if i%2 else 1 )*self.track/self.wheelbase*tan( beta/2 )*robot_speed/self.wheels_radius
				true_speed, torque = controller.update( robot_speed/self.wheels_radius + omega_steer + omega_turn )
				#if i == 0 :
					#print( '%+f %+f' % ( true_speed*180/pi, torque ) )


		# Steering angle control:
		steering_angle = self.local_data['angle']*pi/180

		true_angle, torque = self.steering_controller.update( steering_angle )
		#print( '%+f %+f' % ( true_angle*180/pi, torque ) )


		# SEA control:
		desired_torque = self.local_data['torque']
		#self.sea_hinge_controller.update( desired_torque*pi/180 )

		angle_diff = self.sea_spring.getAngle()

		#sea_speed = self.sea_Kp*( desired_torque - self.sea_stiffness*angle_diff )
		#self.sea_hinge_controller.update( sea_speed )

		target_angle = self.sea_hinge_controller.getAngle() + desired_torque/self.sea_stiffness - angle_diff
		target_angle = min( self.sea_angle_limit, max( -self.sea_angle_limit, target_angle ) )
		self.sea_hinge_controller.update( target_angle )


		# Action of springs:
		self.sea_spring.applyTorque( -self.sea_stiffness*angle_diff )

		leg_torques = []
		for leg in self.torque_sensors :
			leg_torques.append( -self.leg_stiffness*leg.getAngle() )
			leg.applyTorque( leg_torques[-1] )
		#print( leg_torques[0], leg_torques[1], leg_torques[2], leg_torques[3] )


