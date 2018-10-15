#!/usr/bin/python3
from pymorse import Morse
import curses
import os
os.environ.setdefault( 'ESCDELAY', '0' )


try :

	stdscr = curses.initscr()
	curses.noecho()
	stdscr.keypad( True )
	curses.cbreak()
	curses.curs_set( False )

	#while True :

	with Morse() as simu :

		cmd = simu.rover.actuation

		speed = 0.0
		speed_inc = 0.1

		angle = 0.0
		angle_inc = 5
		angle_limit = 50

		torque = 0.0
		torque_inc = 10

		crawling_mode = False

		stdscr.addstr( 0, 0, 'Controls: UP/DOWN/0 LEFT/RIGHT/. +/-/Enter /', curses.A_DIM )

		while True :

			cmd.publish( { 'speed': speed, 'angle': angle, 'torque': torque, 'crawl': crawling_mode } )

			stdscr.addstr( 1, 0, 'Speed: %+.1f m/s | Angle: %+.f° | Torque: %+.1f N.m' % ( speed, angle, torque ) )
			if crawling_mode :
				stdscr.addstr( ' [crawling mode]' )
			stdscr.clrtoeol()
			#stdscr.refresh()

			c = stdscr.getkey()

			if c == 'KEY_UP' :
				speed += speed_inc
			elif c == 'KEY_DOWN' :
				speed -= speed_inc
			elif c == '0' :
				speed = 0

			elif c == 'KEY_LEFT' :
				angle -= angle_inc
				if angle < -angle_limit :
					angle = -angle_limit
			elif c == 'KEY_RIGHT' :
				angle += angle_inc
				if angle > angle_limit :
					angle = angle_limit
			elif c == '.' :
				angle = 0

			elif c == '+' :
				torque += torque_inc
			elif c == '-' :
				torque -= torque_inc
			elif c == '\n' :
				torque = 0

			elif c == '/' :
				crawling_mode = not crawling_mode

			elif c == 'KEY_BACKSPACE' :
				simu.reset()

			elif len( c ) == 1 and ord( c ) == 27 :
				simu.quit()
				break

			#elif c == ' ' :
				#break

			else :
				continue

except KeyboardInterrupt :
	pass

finally :
	curses.endwin()
