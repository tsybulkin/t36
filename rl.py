# this module contains functions related to reinforcement learning
#
#
import random 
import numpy as np


EPS = 0.2
L_RATE = 0.7

U_MAX = 6


def init_Q():
	return np.zeros((21**4, 2*U_MAX+1))


def get_state(dx,a,da,v_target):
	"""returns digitized state
	"""
	return ( d_state(10,dx), d_state(20,a), d_state(10,da), d_state(10,v_target) )



def d_state(scale,x): 
	if x > 0 : return min(10, rd(scale*x))
	else: return max(-10, rd(scale*x))



def rd(y): return int(round(y))



def state2index((dx,a,da,v)):
	return (10 + dx)* 21**3 + (10 + a)* 21**2 + (10 + da)* 21 + (10 + v)



def get_policy_val(state,Q):
	ind = state2index(state)
		
	if random.random() < EPS: u = random.choice(range(-U_MAX, U_MAX+1))
	else: u = np.argmax(Q[ind])
	
	if u > U_MAX: u = u - U_MAX*2 - 1
	return ( Q[ind][u], u )



def get_reward(state,next_state,u): return 0.



def learn(state,u,next_state,Q): pass


