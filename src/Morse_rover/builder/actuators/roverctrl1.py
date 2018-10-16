from morse.builder.creator import ActuatorCreator

class Roverctrl1(ActuatorCreator):
    _classpath = "Morse_rover.actuators.roverctrl1.Roverctrl1"
    _blendname = "roverctrl1"

    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name)

