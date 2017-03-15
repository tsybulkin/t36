import numpy as np
import scipy.linalg
 
def lqr(A,B,Q,R):
    """Solve the continuous time lqr controller.
     
    dx/dt = A x + B u
     
    cost = integral x.T*Q*x + u.T*R*u
    """
    X = np.matrix(scipy.linalg.solve_continuous_are(A, B, Q, R))
     
    K = np.matrix(scipy.linalg.inv(R)*(B.T*X))
     
    eigVals, eigVecs = scipy.linalg.eig(A-B*K)
     
    return K, eigVals



if __name__ == '__main__':
    A = np.array([[0., 1.],
                  [15., 0.]])
    B = np.array([[0.],
                  [3.]])
    
    Q = np.eye(2)
    R = np.array([[1]])

    K, eigenvals = lqr(A,B,Q,R)
    print "K:",K,"\neigen vals:",eigenvals
    