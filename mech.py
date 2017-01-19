from sympy import cos, sin, diff, symbols
from sympy.physics.mechanics import LagrangesMethod, dynamicsymbols


def init_vars(): return dynamicsymbols('x a')

def La(x,a):
	g, mb, mw, h, R, Ib, Iw, K, f, U = symbols('g mb mw h R Ib Iw K f U')
	dx, da = dynamicsymbols('x a',1)

	# wheel angular velocity
	w = dx / R

	# dissipation force
	Q = K*dx

	T = (mb+mw)/2*dx**2 + Ib/2*da**2 + Iw/2*w**2
	V = - mb*h*g*(1-cos(a))

	Eq1 = diff( diff(T,dx),'t') - diff(T,x) + diff(V,x) + Q - f*U / R
	Eq2 = diff( diff(T,da),'t') - diff(T,a) + diff(V,a) + Q*R - f*U

	return (Eq1, Eq2)



def run():
	x,a = init_vars()
	print La(x,a)



if __name__ == '__main__':
	run()



