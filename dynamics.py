"""
This module provides robot simulation functions

The diff equation that governs the robot motion:
	old formulas:
		1)  K*dx + (mb + mw + Iw/R**2)*d2x - U*f/R = 0
		2)  Ib*d2a - K*R*dx + U*f - g*h*mb*a = 0
	
	new formulas:
	1) K*dx - L*mb*sin(a)*da**2 + L*mb*cos(a)*d2a + (Iw/(R**2) + mb + mw)*d2x - U*f/R = 0
	
	2) -L*g*mb*sin(a) + L*mb*cos(a)*d2x + U*f + (Ibc + L**2*mb)*d2a = 0
	
	Ibc - inertia moment w.r.t. center of mass
	Ibc + L**2*mb = Ib


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
from math import exp, sqrt, sin, cos
from numpy import sign, linalg, array
import control
import rl, monte
from matplotlib import pyplot as plt
import sys, random
import cPickle
import os.path
from const import *


def run(time_out=10., epochs=1):
	random.seed()
	tau = 0.001
	
	#if os.path.isfile('q_tab.dat'): Q = get_q_tab()
	#else: 
	#Q = monte.init_Q(time_out/tau)
	

	for ep in range(epochs): 
		if ep%1000 == 0: print "episodes:",ep

		## initial conditions
		x = 0.
		dx = 0.
		a = random.uniform(-0.1, 0.1)
		#da = random.uniform(-0.1, 0.1)		
		da = 0.
		ia = 0.
		
		t = 0.
		log = []
		print "C:", C

		while t < time_out:
			t += tau
			v = v_target(t)
			u = control.control(dx,a,da,ia,v)
			#u = monte.get_policy(state,Q)
			x,dx,a,da = get_next_values(x,dx,a,da,u,tau)
			ia += a*tau
			print "x:",x

			log.append((t,dx,a,v,u))
			#next_state = monte.get_state(dx,a,da)  #,v_target)
			if abs(a) > 0.7: 
				reward = -100.
				#Q = monte.learn(state,u,next_state,reward,Q)
				break
			else:
				#reward = rl.get_reward(state,next_state,u)
				#Q = rl.learn(state,u,next_state,reward,Q)
				#state = next_state
				pass
	
	show(log)
	#save_q_tab(Q)

def v_target(t):
	if t < 30.: return 0.
	elif t < 6: return -0.45
	elif t < 9.: return 0.
	else: return 0.


def show(log):
	[T,X,A,V,U] = zip(*log)
	
	# Two subplots, the axes array is 1-d
	plt.figure(1)
	plt.title('simulation results')
	plt.subplot(311)
	plt.ylabel('robot velocity')
	plt.plot(T,X,'b-',T,V,'--g')

	plt.subplot(312)
	plt.ylabel('robot inclination')
	plt.plot(T,A,'r--')

	plt.subplot(313)
	plt.ylabel('robot control')
	plt.plot(T,U,'k')

	plt.show()
	




def get_next_values(x,dx,a,da,u,tau):
	A11 = Iw/(R**2) + mb + mw
	A12 = L*mb*cos(a)
	A21 = L*mb*cos(a)
	A22 = Ib

	B1 = f*u/R - K*dx + L*mb*sin(a)*da**2
	B2 = L*g*mb*sin(a) - f*u

	A = array([[A11,A12],[A21,A22]])
	B = array([B1,B2])
	d2x, d2a = linalg.inv(A).dot(B)
	
	dx += d2x * tau
	da += d2a * tau

	x += dx * tau
	a += da * tau

	return (x, dx, a, da)



def get_q_tab(): 
	f = open('q_tab.dat')
	Q = cPickle.load(f)
	f.close()
	return Q



def save_q_tab(Q):
	f = open('q_tab.dat','w')
	cPickle.dump(Q,f)
	f.close()




if __name__ == '__main__':
	args = sys.argv
	if len(args) == 1: print "\nUSAGE:\n\tpython dynamics.py run [time] OR\n" +\
				"python dynamics train [N]\n"
	elif len(args) == 2 and args[1] == 'run': run()
	elif len(args) == 3 and args[1] == 'run': 
		t = float(args[2])
		run(time_out=t)
	elif len(args) == 2 and args[1] == 'train': run(epochs=100)
	elif len(args) == 3 and args[1] == 'train': 
		N = int(args[2])
		run(epochs=N)
	else:
		print "\nUSAGE:\n\tpython dynamics.py run [time] OR\n" +\
				"python dynamics train [N]\n"
	
	
	
	

