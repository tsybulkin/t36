"""
This module provides robot simulation functions

The diff equation that governs the robot motion:

	1)  K*dx + (mb + mw + Iw/R**2)*d2x - U*f/R = 0

	2)  Ib*d2a + K*R*dx - U*f - g*h*mb*a = 0

where:
	Iw, Ib - inertia moments of robot body and wheels
	mb, mw - the masses of robot body and wheels
	K - dissipation constant describing the friction of motors
	U - voltage supplied to motors - CONTROL
	f - constant describing the motor torque w.r.t. the voltage supplied
	g - gravitational constant
	h - the lenght between the centre of mass of the robot body and robot wheels axis
	R - robot wheel radius
	x,a - robot coordinate and inclination angle

"""
from math import exp, sqrt
import control
from matplotlib import pyplot as plt

g = 9.81
mb = 15.
mw = 1.
R = 0.16
Iw = 0.5*mw*R**2  # ~solid disk
h = 0.1
Ib = mb*h**2
f = 2.
K = 5.  # can be estimated from maximal motor speed


def run(time_out=1.):
	tau = 0.01 

	## initial conditions
	x = 0.
	dx = 1.0
	a = 0.04
	da = 0.

	t = 0.
	u = 0.
	log = []

	while t < time_out:
		log.append((t,dx,a,u))
		t += tau

		u = control.control(x,dx,a,da)
		x,dx,a,da = get_next_state(x,dx,a,da,u,tau)
		
		if abs(a) > 0.5: break

	T = [ t for (t,_,_,_) in log]
	X = [ dx for (_,dx,_,_) in log]
	A = [ a for (_,_,a,_) in log]
	U = [ u for (_,_,_,u) in log]
	
	# Two subplots, the axes array is 1-d
	plt.figure(1)
	plt.title('simulation results')
	plt.subplot(311)
	plt.ylabel('robot velocity')
	plt.plot(T, X, 'k')

	plt.subplot(312)
	plt.ylabel('robot inclination')
	plt.plot(T, A, 'r--')

	plt.subplot(313)
	plt.ylabel('robot control')
	plt.plot(T,U,'.b')

	plt.show()
	



def get_next_state(x,dx,a,da,u,tau):
	# K*dx + (mb + mw + Iw/R**2)*d2x - u*f/R = 0
	C = mb + mw + Iw/R**2
	dx1 = ( u*f/R + (C/tau - K/2)*dx ) / (C/tau + K/2)
	x1 = x + dx1*tau

	# Ib*d2a + K*R*dx - U*f - g*h*mb*a = 0
	da1 = da + (-u*f + g*h*mb*a + K*R*dx1)*tau / Ib
	a1 = a + da1*tau 

	return (x1, dx1, a1, da1)



if __name__ == '__main__':
	run()




