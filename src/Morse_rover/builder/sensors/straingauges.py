from morse.builder.creator import SensorCreator

class Straingauges(SensorCreator):
    _classpath = "Morse_rover.sensors.straingauges.Straingauges"
    _blendname = "straingauges"

    def __init__(self, name=None):
        SensorCreator.__init__(self, name)

