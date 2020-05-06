from morse.builder.creator import ActuatorCreator

class Terramechanics(ActuatorCreator):
	_classpath = "Morse_rover.actuators.terramechanics.Terramechanics"
	_blendname = "terramechanics"

	def __init__(self, name=None):
		ActuatorCreator.__init__(self, name)

		self.frequency( 10000 )


