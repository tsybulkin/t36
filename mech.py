from sympy import cos, sin, diff, symbols
from sympy.physics.mechanics import LagrangesMethod, dynamicsymbols


def init_vars(): return dynamicsymbols('x a')

def La(x,a):
	g, mb, mw, h, R, Ib, Iw = symbols('g mb mw h R Ib Iw')
	dx, da = dynamicsymbols('x a',1)

	# wheel angular velocity
	w = dx / R


	T = (mb+mw)/2*dx**2 + Ib/2*da**2 + Iw/2*w**2
	V = mb*h*g*(1-cos(a))

	return T-V



