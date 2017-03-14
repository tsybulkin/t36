
from const import *
from math import sqrt
import numpy as np 

U_MAX = 9.


def control(dx,a,da,ia,v): 
	da = da 
	dx = dx 
	#min(3,abs(da + 0.25*a*C**2 - (v_target-dx)*0.9 ))*sign(da + a*C**2)
	#u = (2*(a+limit((dx-v)*0.2,0.15))*C**2 + 10*da) * Ib/f #+ (dx-v)
	u = (1.5*a*C**2 + 15*da) * Ib/f + 70*ia #+ (dx-v)
	#u = 69.*a + 14.*da + 0.01*ia
	return limit(u,U_MAX)
	


def limit(u,limit_u):
	if u > 0: return min(u, limit_u)
	else: return max(u, -limit_u)


def sign(x): 
	if x > 0: return 1.
	elif x < 0: return -1.
	else: return 0. 