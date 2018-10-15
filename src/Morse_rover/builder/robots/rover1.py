from morse.builder import *
from Morse_rover.builder.actuators import Roverctrl


class Rover1( Robot ):
	"""
	First version of the 2 DOF rover, with a roverctrl and a pose sensor.
	"""
	def __init__( self, name=None, debug=True ):

		Robot.__init__( self, name=name )
		self.properties( classpath = "Morse_rover.robots.rover1.Rover1" )

		import rover_C2
		#rover_filename = 'rover_C2.py'
		#exec( open( os.path.dirname( os.path.abspath( __file__ ) ) + '/../../../../' + rover_filename ).read() )


		###################################
		# Actuators
		###################################

		self.actuation = Roverctrl()
		self.append( self.actuation )

		# Optionally allow to move the robot with the keyboard
		#if debug:
			#keyboard = Keyboard()
			#keyboard.properties( ControlType = 'Position' )
			#self.append( keyboard )


		###################################
		# Sensors
		###################################

		#self.pose = Pose()
		#self.append( self.pose )
	
	def translate( self, x, y, z ) :

		import bpy
		bpy.ops.object.select_all( action='SELECT' )
		bpy.ops.transform.translate( value=( x, y, z ) )
	
	def rotate( self, angle, axis ) :

		import bpy
		bpy.ops.object.select_all( action='SELECT' )
		bpy.ops.transform.rotate( value=angle, axis=axis )


