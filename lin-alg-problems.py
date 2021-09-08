# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 08:28:45 2021

@author: sahil
"""

import numpy as np

"""
Linear Algebra Problems
"""

"""
HW-1 Q1
A bank makes four kinds of loans to its customers and these loans yield the following annual interest rates to the bank:

• First mortgage 14%
• Second mortgage 20%
• Home improvement 20%

• Personal overdraft 10%

We are interested in the bank’s lending strategy. The information we know is as following:

1. In total $250 million is lent out.
2. First mortgages are 55% of all mortgages (i.e. first and second mortgage) issued.

3. Second mortgages are 25% of all loans issued.
4. The dollar-weighted average interest rate on all loans is 15%.

Calculate the lending strategy using matrix inversion.  How much is lent in home improvement loans?
"""

A1 = np.array([[1,1,1,1],
              [45,-55,0,0],
              [-25,75,-25,-25],
              [14,20,20,10]])
b1 = np.array([250,0,0,3750])

x1 = np.linalg.solve(A1,b1)

print("${0:.2f} is lent in home improvements".format(x1[2]))


"""
Total amount invested is 50000 USD in 3 funds with interest rates 6%, 8%, 10%
Total interest in 1 year is 3700 USD
Money invested at 6% is twice the money invested at 10%
Solve for 3 funds
"""

A2 = np.array([[6,8,10],
             [1,1,1],
             [1,0,-2]])
b2 = np.array([370000,50000,0])

x2 = np.linalg.solve(A2,b2)

for i in range(len(x2)):
    print("Money invested in Fund {0} is ${1:.0f}".format(i+1,x2[i]))
