"""
This module provides robot simulation functions

The diff equation that governs the robot motion:

	1)  K*dx + (mb + mw + Iw/R**2)*d2x - U*f/R = 0

	2)  Ib*d2a - K*R*dx + U*f - g*h*mb*a = 0

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
import rl
from matplotlib import pyplot as plt
import sys, random
import cPickle
import os.path


g = 9.81
mb = 15.
mw = 1.
R = 0.16
Iw = 0.5*mw*R**2  # ~solid disk
h = 0.1
Ib = mb*h**2
f = 2.
K = 5.  # can be estimated from maximal motor speed


def run(time_out=3., epochs=1):
	tau = 0.01
	if os.path.isfile('q_tab.dat'): Q = get_q_tab()
	else: 
		Q = rl.init_Q()

	for ep in range(epochs): 
		if ep%100 == 0: print "epoch:",ep

		## initial conditions
		x = 0.
		dx = random.uniform(0., 3.,)
		a = random.gauss(0., 0.1)
		da = 0.
		v_target = random.choice([0.,1.,2.,3.])
		
		t = 0.
		log = []
		state = rl.get_state(dx,a,da,v_target)
			
		while t < time_out:
			t += tau

			u,val = rl.get_policy_val(state,Q)
			x,dx,a,da = get_next_values(x,dx,a,da,u,tau)
			next_state = rl.get_state(dx,a,da,v_target)
			reward = rl.get_reward(state,next_state,u)
			rl.learn(state,u,next_state,Q)
			state = next_state

			log.append((t,dx,a,u))
			
			if abs(a) > 0.7: break

	show(log)
	save_q_tab(Q)



def show(log):
	[T,X,A,U] = zip(*log)
	
	# Two subplots, the axes array is 1-d
	plt.figure(1)
	plt.title('simulation results')
	plt.subplot(311)
	plt.ylabel('robot velocity')
	plt.plot(T,X,'k')

	plt.subplot(312)
	plt.ylabel('robot inclination')
	plt.plot(T,A,'r--')

	plt.subplot(313)
	plt.ylabel('robot control')
	plt.plot(T,U,'.b')

	plt.show()
	




def get_next_values(x,dx,a,da,u,tau):
	# K*dx + (mb + mw + Iw/R**2)*d2x - u*f/R = 0
	C = mb + mw + Iw/R**2
	dx1 = ( u*f/R + (C/tau - K/2)*dx ) / (C/tau + K/2)
	x1 = x + dx1*tau

	# Ib*d2a + K*R*dx - U*f - g*h*mb*a = 0
	da1 = da + (-u*f + g*h*mb*a + K*R*dx1)*tau / Ib
	a1 = a + da1*tau 

	return (x1, dx1, a1, da1)



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
	elif len(args) == 2 and args[1] == 'train': train()
	elif len(args) == 3 and args[1] == 'train': 
		N = int(args[2])
		train(epochs=N)
	else:
		print "\nUSAGE:\n\tpython dynamics.py run [time] OR\n" +\
				"python dynamics train [N]\n"
	
	
	
	

