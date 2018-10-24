from morse.builder.creator import ActuatorCreator

class Roverctrl2(ActuatorCreator):
	_classpath = "Morse_rover.actuators.roverctrl2.Roverctrl2"
	_blendname = "roverctrl2"

	def __init__(self, name=None):
		ActuatorCreator.__init__(self, name)

		self.frequency( 1000 )


