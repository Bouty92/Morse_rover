#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <Morse_rover> environment

Feel free to edit this template as you like!
"""

from morse.builder import *
from Morse_rover.builder.robots import Rover1, Rover2
from Morse_rover.builder.sensors import Screenshots


# Add the MORSE mascott, MORSY.
# Out-the-box available robots are listed here:
# http://www.openrobots.org/morse/doc/stable/components_library.html
#
# 'morse add robot <name> Morse_rover' can help you to build custom robots.
rover = Rover1()
#rover = Rover2()
rover.translate( 0, 0, 0.1 )
#rover.rotate( 180, ( 0, 0, 1 ) )
#screenshots = Screenshots()
#rover.append( screenshots )

# The list of the main methods to manipulate your components
# is here: http://www.openrobots.org/morse/doc/stable/user/builder_overview.html

# Add a motion controller
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
#
# 'morse add actuator <name> Morse_rover' can help you with the creation of a custom
# actuator.
#motion = MotionVW()
#robot.append(motion)


# Add a keyboard controller to move the robot with arrow keys.
#keyboard = Keyboard()
#robot.append(keyboard)
#keyboard.properties(ControlType = 'Position')

# Add a pose sensor that exports the current location and orientation
# of the robot in the world frame
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#sensors
#
# 'morse add sensor <name> Morse_rover' can help you with the creation of a custom
# sensor.
#pose = Pose()
#robot.append(pose)

# To ease development and debugging, we add a socket interface to our robot.
#
# Check here: http://www.openrobots.org/morse/doc/stable/user/integration.html 
# the other available interfaces (like ROS, YARP...)
rover.add_default_interface( 'socket' )


# set 'fastmode' to True to switch to wireframe mode
#env = Environment( 'outdoors', fastmode=False )
#env = Environment( './mars_scene.blend', fastmode=False )
env = Environment( './scene_1.blend', fastmode=False )
#env = Environment( './scene_2.blend', fastmode=False )

env.set_time_strategy( TimeStrategies.FixedSimulationStep )
#env.simulator_frequency( 60 )
#env.simulator_frequency( 100, 5, 5 )
env.simulator_frequency( 200, 5, 5 )
#env.simulator_frequency( 200, 1, 1 )
#env.set_physics_step_sub( 5 )
#env.show_framerate()
#env.show_physics()

#env.fullscreen()

#env.set_camera_location( [ -2, -1, 1 ] )
#env.set_camera_rotation( [ 1.3, 0, -1.1 ] )

#env.set_camera_location( [ 0.5, -2, 1 ] )
#env.set_camera_rotation( [ 1.2, 0, -0.5 ] )

env.set_camera_location( [ -0.8, -1.1, 0.6 ] )
env.set_camera_rotation( [ 1.3, 0, -0.8 ] )

#env.set_camera_location( [ -0.6, -0.9, 0.8 ] )
#env.set_camera_rotation( [ 1, 0, -0.6 ] )


