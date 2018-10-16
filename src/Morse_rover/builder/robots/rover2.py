from morse.builder import *
from Morse_rover.builder.actuators import Roverctrl2
from Morse_rover.builder.sensors import Straingauges


class Rover2( Robot ):
	"""
	Second version of the rover with flexible wheel axles and straingauges sensor.
	"""
	def __init__( self, name=None, debug=True ):

		Robot.__init__( self, name=name )
		self.properties( classpath = "Morse_rover.robots.rover2.Rover2" )

		import rover_C3
		#rover_filename = 'rover_C3.py'
		#exec( open( os.path.dirname( os.path.abspath( __file__ ) ) + '/../../../../' + rover_filename ).read() )


		###################################
		# Actuators
		###################################

		self.actuation = Roverctrl2()
		self.append( self.actuation )

		# Optionally allow to move the robot with the keyboard
		#if debug:
			#keyboard = Keyboard()
			#keyboard.properties( ControlType = 'Position' )
			#self.append( keyboard )


		###################################
		# Sensors
		###################################

		self.gauges = Straingauges()
		self.append( self.gauges )

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


