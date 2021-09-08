# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 19:54:51 2021

@author: sahil
"""

import numpy as np


"""
Generate a Lehmer Matrix
A(i,j) = i/j if j > i and A(i,j) = j/i otherwise
"""

A = np.zeros((20,20))

for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        #print("i -> {0} ... j -> {1}".format(i,j))
        if j > i:
            A[i,j] = (i+1)/(j+1)
        else:
            A[i,j] = (j+1)/(i+1)
            
print((A == A.T).all())

"""
Assign inverse of A to C
Assign [1 2 3 4 5 6 7 8 9 10 10 9 8 7 6 5 4 3 2 1] to d
Solve for x in Ax = Cd
"""

C = np.linalg.inv(A)
d = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
Cd = np.dot(C,d)
x = np.linalg.solve(A,Cd)

"""
What is x[9] ?
"""

print(x[9])