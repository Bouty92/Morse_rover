from morse.builder.creator import ActuatorCreator

class Roverctrl(ActuatorCreator):
    _classpath = "Morse_rover.actuators.roverctrl.Roverctrl"
    _blendname = "roverctrl"

    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name)

