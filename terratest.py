#!/usr/bin/python3
from numpy import *
from matplotlib.pyplot import *


class Terratest() :

	def __init__( self ) :

		# Wheel radius:
		self.r = 0.15

		# Wheel width:
		self.b = 0.1

		# Parameters of the velocity field:
		self.alpha1 = 0.64 #m^-1
		self.alpha2 = 0.03
		self.alpha3 = 35 #m^-1

		# Parameters of the elastoplastic model:
		E = 3e6 #Pa
		nu = 0.32
		self.C = array([ [ 1 - nu, nu, 0 ], [ nu, 1 - nu, 0 ], [ 0, 0, 1 - 2*nu ] ])*E/( 1 + nu )/( 1 - 2*nu )
		self.beta = 41*pi/180
		self.d = 350 #Pa
		self.Re = 0.15
		self.epvol0 = 0.001
		self.alpha = 0.01
		self.Kcos = 1 + self.alpha - self.alpha/cos( self.beta )
		self.tanbeta = tan( self.beta )

		# Harderning pattern for the elastoplastic model:
		epvol_pb_values = { 0.15 : 0, 1.5 : 0.014661, 3 : 0.028334, 6 : 0.053024, 9 : 0.074619, 12 : 0.093572, 15 : 0.110262, 18 : 0.125006, 21 : 0.138069, \
                            24 : 0.149679, 27 : 0.160028, 30 : 0.16928, 36 : 0.185036, 48 : 0.208422, 63 : 0.228045, 87 : 0.248232, 120 : 0.266976, 150 : 0.280999 }
		self.epvol_pb_table = sorted( epvol_pb_values.items(), reverse=True )

		# Tolerance of the return-mapping algorithm:
		self.TOL = 0.01

		# Maximum number of iterations for the return-mapping algorithm:
		self.maxiter = 1000

		# Number of mesh points:
		self.mesh_resolution = 100

		self.thetas = linspace( 0, 2*pi, self.mesh_resolution + 1 )[:-1]
		self.meshPoints_coord = self.r*array([ sin( self.thetas ), [0]*self.mesh_resolution, -cos( self.thetas ) ])
		self.ee = [zeros(3)]*self.mesh_resolution
		self.ep = [zeros(3)]*self.mesh_resolution
		self.pb = [self.epvol0]*self.mesh_resolution
		self.sigma = [zeros(3)]*self.mesh_resolution


	def Pb( self, ep ) :
		
		epvol = max( ep[0] + ep[1], self.epvol0 )

		table = self.epvol_pb_table
		i = 1
		while epvol < table[i][0] and i < len( table ) - 1 :
			i += 1

		return ( table[i-1][1] + ( table[i][1] - table[i-1][1] )/float( table[i][0] - table[i-1][0] )*( epvol - table[i-1][0] ) )*1e3
	

	def F( self, sigma, pb ) :

		#print( '		', end='' )
		#print( sigma, pb )
		pa = ( pb - self.Re*self.d )/( 1 + self.Re*tan( self.beta ) )
		Ktan = self.d + pa*self.tanbeta

		p = -( sigma[0] + sigma[1] )/3
		q = sqrt( 5./6*( sigma[0]**2 + sigma[1]**2 ) - 4./3*sigma[0]*sigma[1] + 3*sigma[2]**2 )
		#print( '		pa: %f p: %f q: %f' % ( pa, p, q ) )

		if p >= pa :
			
			return sqrt( ( p - pa )**2 + ( self.Re*q/self.Kcos )**2 ) - self.Re*Ktan

		elif p + self.beta*( q + abs( self.Re*q/self.Kcos ) - ( self.Re + self.alpha )*Ktan ) - pa > 0 :
			
			return sqrt( ( p - pa )**2 + ( q - ( 1 - self.alpha/cos( self.alpha ) )*Ktan )**2 ) - self.alpha*Ktan

		else :
			
			return q - p*self.tanbeta - self.d


	def gradF( self, sigma, pb, F=None ) :

		pa = ( pb - self.Re*self.d )/( 1 + self.Re*tan( self.beta ) )
		Ktan = self.d + pa*self.tanbeta

		p = -( sigma[0] + sigma[1] )/3
		q = sqrt( 5./6*( sigma[0]**2 + sigma[1]**2 ) - 4./3*sigma[0]*sigma[1] + 3*sigma[2]**2 )

		if p >= pa :

			if F is None :
				F = self.F( sigma, pb )

			Kq = ( self.Re/self.Kcos )**2
			dFc11 = ( 2./3*( pa - p ) + Kq*( 5./3*sigma[0] - 4./3*sigma[1] ) )/2/F
			dFc22 = ( 2./3*( pa - p ) + Kq*( 5./3*sigma[1] - 4./3*sigma[0] ) )/2/F
			dFc12 = Kq*3*sigma[2]/F
			
			return array([ dFc11, dFc22, dFc12 ])

		elif p + self.beta*( q + abs( self.Re*q/self.Kcos ) - ( self.Re + self.alpha )*Ktan ) - pa > 0 :

			if F is None :
				F = self.F( sigma, pb )

			Kq = q - ( 1 - self.alpha/cos( self.alpha ) )*Ktan
			dFtr11 = ( 2./3*( pa - p ) + Kq*( 5./3*sigma[0] - 4./3*sigma[1] )/q )/2/F
			dFtr22 = ( 2./3*( pa - p ) + Kq*( 5./3*sigma[1] - 4./3*sigma[0] )/q )/2/F
			dFtr12 = Kq*3*sigma[2]/q/F
			
			return array([ dFtr11, dFtr22, dFtr12 ])

		else :
			
			dFs11 = ( 5./3*sigma[0] - 4./3*sigma[1] )/2/q - self.tanbeta/3
			dFs22 = ( 5./3*sigma[1] - 4./3*sigma[0] )/2/q - self.tanbeta/3
			dFs12 = 3*sigma[2]/q

			return array([ dFs11, dFs22, dFs12 ])


	def gradG( self, sigma, pb ) :

		pa = ( pb - self.Re*self.d )/( 1 + self.Re*tan( self.beta ) )

		p = -( sigma[0] + sigma[1] )/3
		q = sqrt( 5./6*( sigma[0]**2 + sigma[1]**2 ) - 4./3*sigma[0]*sigma[1] + 3*sigma[2]**2 )

		if p >= pa :

			Kq = ( self.Re/self.Kcos )**2
			Gc = sqrt( ( p - pa )**2 + Kq*q**2 )

			dGc11 = ( 2./3*( pa - p ) + Kq*( 5./3*sigma[0] - 4./3*sigma[1] ) )/2/Gc
			dGc22 = ( 2./3*( pa - p ) + Kq*( 5./3*sigma[1] - 4./3*sigma[0] ) )/2/Gc
			dGc12 = Kq*3*sigma[2]/Gc
			
			return array([ dGc11, dGc22, dGc12 ])

		else :

			Kq = ( 1/self.Kcos )**2
			Gs = sqrt( ( ( p - pa )*self.tanbeta )**2 + Kq*q**2 )

			dGs11 = ( 2./3*( pa - p )*self.tanbeta**2 + Kq*( 5./3*sigma[0] - 4./3*sigma[1] )/q )/2/Gs
			dGs22 = ( 2./3*( pa - p )*self.tanbeta**2 + Kq*( 5./3*sigma[1] - 4./3*sigma[0] )/q )/2/Gs
			dGs12 = Kq*3*sigma[2]/q/Gs
			
			return array([ dGs11, dGs22, dGs12 ])


	def test( self ) :

		et_list = [ 0.001 ]
		#et_list = linspace( 0, 0.001, self.mesh_resolution )

		for i in range( len( et_list ) ) :

			Delta_et = zeros( 3 )
			Delta_et[0] = et_list[i]

			#print( Delta_et )

			# Computation of the elastic and plastic parts of the strain increment:
			self.ee[i] = self.ee[i] + Delta_et
			self.sigma[i] = self.C.dot( self.ee[i] )
			F = self.F( self.sigma[i], self.pb[i] )
			#print( '	F: %f' % F )
			niter = 0
			if F > 0 :
				for niter in range( self.maxiter ) :
					dG = self.gradG( self.sigma[i], self.pb[i] )
					Delta_lambda = F/self.gradF( self.sigma[i], self.pb[i], F ).dot( self.C ).dot( dG )
					#print( '	Dlambda: %g' % Delta_lambda )
					Delta_ep = Delta_lambda*dG
					self.ep[i] = self.ep[i] + Delta_ep
					self.ee[i] = self.ee[i] - Delta_ep
					#print( '	', end='' )
					#print( Delta_ep, self.ep[i], self.ee[i] )
					self.sigma[i] = self.sigma[i] - self.C.dot( Delta_ep )
					self.pb[i] = self.Pb( self.ep[i] )

					F = self.F( self.sigma[i], self.pb[i] )
					#print( '	F: %f' % F )
					#print( F )
					if F <= self.TOL :
						break

			print( niter )

		#figure( 'xy' )
		#plot( et_list, [ s[2] for s in self.sigma ] )
		#figure( 'yy' )
		#plot( et_list, [ s[1] for s in self.sigma ] )
		#figure( 'xx' )
		#plot( et_list, [ s[0] for s in self.sigma ] )
		#show()



Terratest().test()
