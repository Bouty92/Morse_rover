#!/usr/bin/python3
from pymorse import Morse
from numpy import mean


class crossing_control() :

	def __init__( self, topic ) :

		self.turning_rate = 15
		self.torque_modulation = 30

		self.da = 1
		self.db = 1
		self.sa = 0.5
		self.sb = 0.5

		self.speed = 0.2
		self.angle = 0
		self.torque = 0
		self.crawling_mode = False

		self.topic = topic

	def default( self ) :
		self.angle = 0
		self.torque = 0
		print( 'DEFAULT' )
	def release_1( self ) :
		self.angle = 0
		self.torque = -self.torque_modulation
		print( 'RELEASE 1' )
	def release_2( self ) :
		self.angle = 0
		self.torque = self.torque_modulation
		print( 'RELEASE 2' )
	def release_3( self ) :
		self.angle = 0
		self.torque = self.torque_modulation
		print( 'RELEASE 3' )
	def release_4( self ) :
		self.angle = 0
		self.torque = -self.torque_modulation
		print( 'RELEASE 4' )
	def rot_left( self ) :
		self.angle = -self.turning_rate
		self.torque = 0
		print( 'ROT LEFT' )
	def rot_right( self ) :
		self.angle = self.turning_rate
		self.torque = 0
		print( 'ROT RIGHT' )
	
	def update( self, f ) :

		i = f.index( min( f ) )

		if i == 0 :
			if f[0] < f[1] - self.da :
				self.release_1()
			else :
				#if f[1] < -self.sa :
				if mean( f[0:2] ) - mean( f[2:4] ) < -self.sa :
					self.rot_left()
				else :
					self.default()
		elif i == 1 :
			if f[1] < f[0] - self.da :
				self.release_2()
			else :
				#if f[0] < -self.sa :
				if mean( f[0:2] ) - mean( f[2:4] ) < -self.sa :
					self.rot_right()
				else :
					self.default()
		elif i == 2 :
			if f[2] < f[3] - self.db :
				self.release_3()
			else :
				#if f[3] < -self.sb :
				if mean( f[2:4] ) - mean( f[0:2] ) < -self.sa :
					self.rot_right()
				else :
					self.default()
		elif i == 3 :
			if f[3] < f[2] - self.db :
				self.release_4()
			else :
				#if f[2] < -self.sb :
				if mean( f[2:4] ) - mean( f[0:2] ) < -self.sa :
					self.rot_left()
				else :
					self.default()

		self.topic.publish( { 'speed': self.speed, 'angle': self.angle, 'torque': self.torque, 'crawl': self.crawling_mode } )


with Morse() as simu :

	cmd = simu.rover.actuation
	torques = simu.rover.gauges

	control = crossing_control( cmd )

	while simu.is_up() :

		t = torques.get()['torques']
		print( t[0], t[1], t[2], t[3] )

		control.update( t )

		simu.sleep( 0.2 )


