from math import sqrt

g = 9.81
mb = 0.9
mw = 0.040
R = 0.0408
Iw = 0.5*mw*R**2  # ~solid disk
L = 0.103
Ib = 0.014
f = 0.01
#K = 5.  # can be estimated from maximal motor speed
K = 0.5
C = sqrt(g*L*mb/Ib)

