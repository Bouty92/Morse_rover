from morse.builder.creator import SensorCreator

class Screenshots(SensorCreator):
	_classpath = "Morse_rover.sensors.screenshots.Screenshots"
	_blendname = "screenshots"

	def __init__(self, name=None):
		SensorCreator.__init__(self, name)

		self.frequency( 25 )
