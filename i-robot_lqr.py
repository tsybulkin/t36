# i-robot
#
# C*dq/dt = A*q + B*u
# dq/dt = C'*A*q + C'*B*u

import lqr
import numpy as np


def solve():
	Iw = 0.
	Ib = 0.014
	mb = 0.9
	mw = 0.
	L = 0.103
	K = 0.5
	f = 0.01
	R = 0.0408
	g = 9.81

	A11 = Iw/R**2 + mb + mw
	A12 = L*mb
	A21 = L*mb
	A22 = Ib

	C = np.array([[0., A11, 0., A12],
				  [1., 0., 0., 0.],
				  [0., A21, 0., A22],
				  [0., 0., 1., 0.]])

	A = np.array([[0., -K, A12, 0.],
				  [0., 1., 0., 0.],
				  [0., 0., A12*g, 0.],
				  [0., 0., 0., 1.]])

	B = np.array([[f/R],
					[0.],
					[-f],
					[0.]])
	Cinv = np.linalg.inv(C)

	Q = np.eye(4)
	R = np.eye(1)
	
	S, eigenvals = lqr.lqr(Cinv.dot(A), Cinv.dot(B), Q, R)
	print "S:",S,"\neigen vals:",eigenvals
    
if __name__ == '__main__':
	solve()
