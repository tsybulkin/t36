# this module contains functions related to reinforcement learning
#
#
import random 
import numpy as np


EPS = 0.2
L_RATE = 0.7
GAMMA = 0.97

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
		
	probs = softmax(Q[ind])
	#print probs
	u = weighted_choice(probs)

	if u > U_MAX: u = u - U_MAX*2 - 1
	#print 'control:',u
	return ( u,Q[ind][u] )



def get_reward(state,next_state,u):
	(dx,_,_,v) = next_state
	return 10 - abs(u) - abs(dx-v)



def learn(state,u,next_state,reward,Q): 
	ind = state2index(state)
	ind1 = state2index(next_state)
	Val = np.max(Q[ind1])
	Q[ind][u] = (1 - L_RATE)*Q[ind][u] + L_RATE*(reward + GAMMA*Val)
	

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x) / np.sum(np.exp(x), axis=0)



def weighted_choice(ps):
	s = 0.
	for i in range(len(ps)):
		s += ps[i]
		if random.random() < s: return i
	return len(ps)



