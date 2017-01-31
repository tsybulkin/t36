# this module contains functions related to reinforcement learning
#
#
import random 
import numpy as np
from dynamics import C


EPS = 0.2
L_RATE = 0.7
GAMMA = 0.97

U_MAX = 3
dx_MAX = 10
a_MAX = 20
da_MAX = 20
v_MAX = 5




def init_Q():
	return 200 * np.ones((2*dx_MAX+1, 2*a_MAX+1, 2*da_MAX+1,2*v_MAX+1, 2*U_MAX+1))


def get_state(dx,a,da,v_target):
	"""returns digitized state
	"""
	return ( d_state(3., dx, dx_MAX), 
			d_state(20., a, a_MAX), 
			d_state(10., da, da_MAX), 
			d_state(1., v_target, v_MAX) )



def d_state(scale,x,Max): 
	if x > 0 : return min(Max, rd(scale*x))
	else: return max(-Max, rd(scale*x))



def rd(y): return int(round(y))




def get_policy(state,Q):
	dx,a,da,v = state
		
	probs = softmax(Q[dx,a,da,v,:])
	u = weighted_choice(probs)

	if u > U_MAX: u = u - U_MAX*2 - 1
	print "policy:",u
	return min(U_MAX,np.abs(da + a*C**2))*np.sign(da + a*C**2)



def get_reward(state,next_state,u):
	(dx,a,da,v) = next_state
	return 3 -0.2*abs(u) -abs(dx-v) -abs(a/20 + da/C/10) # 20 and 10 were scale factors



def learn(state,u,next_state,reward,Q): 
	dx1,a1,da1,v1 = state
	dx2,a2,da2,v2 = next_state

	print "state:",state
	print "next_state:",next_state
	Val = np.max(Q[dx2,a2,da2,v2,:])
	print "Q-value of next state:", Val
	print "old Q-value of state:", Q[dx1,a1,da1,v1,u]
	Q[dx1,a1,da1,v1,u] = (1 - L_RATE)*Q[dx1,a1,da1,v1,u] + L_RATE*(reward + GAMMA*Val)
	print "new Q-values of state:", Q[dx1,a1,da1,v1], "\n"
	return Q


	

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    y = 0.01 * x
    return np.exp(y) / np.sum(np.exp(y), axis=0)



def weighted_choice(ps):
	s = 0.
	for i in range(len(ps)):
		s += ps[i]
		if random.random() < s: return i
	return i



