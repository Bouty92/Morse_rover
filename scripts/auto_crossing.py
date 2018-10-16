#!/usr/bin/python3
from pymorse import Morse


with Morse() as simu :

	cmd = simu.rover.actuation
	torques = simu.rover.gauges

	speed = 0.2
	angle = 0
	torque = 0
	crawling_mode = False

	cmd.publish( { 'speed': speed, 'angle': angle, 'torque': torque, 'crawl': crawling_mode } )

	while True :

		t = torques.get()['torques']
		print( t[0], t[1], t[2], t[3] )


