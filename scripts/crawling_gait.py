#!/usr/bin/python3
from pymorse import Morse
from numpy import mean


with Morse() as simu :

	cmd = simu.rover.actuation
	#torques = simu.rover.gauges

	rot_speed = 30
	torque_modulation = 50
	step_time = 2

	angle = rot_speed
	torque = -torque_modulation

	cmd.publish( { 'speed': 0, 'angle': angle, 'torque': torque, 'crawl': True } )

	simu.sleep( step_time/2 )

	while simu.is_up() :

		#t = torques.get()['torques']
		#print( t[0], t[1], t[2], t[3] )

		angle = -rot_speed
		torque = torque_modulation

		cmd.publish( { 'speed': 0, 'angle': angle, 'torque': torque, 'crawl': False } )

		simu.sleep( step_time )

		angle = rot_speed
		torque = -torque_modulation

		cmd.publish( { 'speed': 0, 'angle': angle, 'torque': torque, 'crawl': True } )

		simu.sleep( step_time )


