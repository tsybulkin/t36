
import cPickle

Q = cPickle.load(open('q_tab.dat'))


def control(x,dx,a,da,v): 
	state = get_state(v-dx,a,da)
	return Q.get(state, 0.)



def get_state(dv,a,da):
	"""returns digitized state
	"""
	return ( d_state(10,dv), d_state(50,a),d_state(10,da) )



def d_state(D,x): 
	if x > 0 : return min(D, rd(x))
	else: return max(-D, rd(x))



def rd(y): return int(round(y))
