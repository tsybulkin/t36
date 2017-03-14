from sympy import cos, sin, diff, symbols
from sympy.physics.mechanics import LagrangesMethod, dynamicsymbols


def init_vars(): return dynamicsymbols('x a')

def La(x,a):
	g, mb, mw, L, R, Ib, Iw, K, f, U = symbols('g mb mw L R Ib Iw K f U')
	dx, da = dynamicsymbols('x a',1)

	# wheel angular velocity
	w = dx / R

	# dissipation force
	Q = -K*dx

	T = (mb/2 + mw/2 + Iw/2/R**2)*dx**2 + mb*L*cos(a)*dx*da + (mb*L**2 + Ib)/2*da**2
	V = mb*L*g*cos(a)

	Eq1 = diff( diff(T-V,dx),'t') - diff(T-V,x) - Q - f*U / R
	Eq2 = diff( diff(T-V,da),'t') - diff(T-V,a) + f*U

	return (Eq1, Eq2)



def run():
	x,a = init_vars()
	Eq1,Eq2 = La(x,a)
	print "Eq1:", Eq1
	print "\nEq2:", Eq2




if __name__ == '__main__':
	run()



