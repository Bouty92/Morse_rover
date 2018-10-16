import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.sensor

from morse.core.services import service, async_service
from morse.core import status
from morse.helpers.components import add_data, add_property

from Morse_rover.actuators.roverctrl1 import hingeController


class Straingauges(morse.core.sensor.Sensor):
	"""Write here the general documentation of your sensor.
	It will appear in the generated online documentation.
	"""
	_name = "Straingauges"
	_short_desc = ""

	# define here the data fields exported by your sensor
	# format is: field name, default initial value, type, description
	add_data( 'torques', [], 'list', 'List of 4 torques measured above each wheel' )


	def __init__(self, obj, parent=None):
		logger.info("%s initialization" % obj.name)
		# Call the constructor of the parent class
		morse.core.sensor.Sensor.__init__(self, obj, parent)

		self.scene = parent.bge_object.scene

		#for obj in self.scene.objects :
			#print( obj.name )

		self.front_frame = self.scene.objects['front frame']
		self.boggie = self.scene.objects['boggie']

		self.wheels = []
		for i in range( 4 ) :
			self.wheels.append( self.scene.objects['wheel ' + str( i + 1 )] )
		self.axles = []
		for i in range( 4 ) :
			self.axles.append( self.scene.objects['axles ' + str( i + 1 )] )

		self.leg_stiffness = 200
		self.torque_sensors = []
		for i in range( 4 ) :
			self.torque_sensors.append( hingeController( self.axles[i], ( self.front_frame if i < 2 else self.boggie ), ( 0, 1, 0 ) ) )

	@service
	def get_current_distance(self):
		""" This is a sample (blocking) service (use 'async_service' decorator
		for non-blocking ones).

		Simply returns the value of the internal counter.

		You can access it as a RPC service from clients.
		"""
		#logger.info("%s is %sm away" % (self.name, self.local_data['distance']))

		#return self.local_data['distance']

	def default_action(self):
		""" Main loop of the sensor.

		Implements the component behaviour
		"""

		leg_torques = []
		for leg in self.torque_sensors :
			leg_torques.append( -self.leg_stiffness*leg.getAngle() )
			#leg.applyTorque( leg_torques[-1] )
		#print( leg_torques[0], leg_torques[1], leg_torques[2], leg_torques[3] )

		self.local_data['torques'] = leg_torques


