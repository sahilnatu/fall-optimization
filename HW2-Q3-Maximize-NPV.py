# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 13:58:49 2021

@author: sahil
"""

import numpy as np
import gurobipy as gp

# Q3
#
# Star Oil Company is considering five different investment opportunities. The table
# below gives the required cash outflows and net present values in millions of dollars.
# Star Oil has $40 million available for investment now (time 0); it estimates that
# one year from now (time 1) $20 million will be available for investment. Star Oil
# may purchase any fraction of each investment, but no more than 100% of each opportunity.
# In this case, the cash outflows and NPV are adjusted accordingly.
#
# For example, if Star Oil purchases one-fifth of investment 3, then a cash outflow
# of 1/5 × 5 = 1 million dollars would be required at time 0, and a cash outflow of
# 1/5 × 5 = 1 million would be required at time 1. The one-fifth share of investment
# three would yield an NPV of 1/5 ∗ 16 = 3.2 million dollars. Star Oil wants to maximize
# the NPV that can be obtained by investing in investments 1-5. Formulate an LP that
# will help achieve this goal. Assume that any funds leftover at time 0 cannot be used
# at time 1.
#
# What percentage of opportunity 3 should be Star Oil invest in?  Answer in decimals,
# so if your answer is 54%, you should input 0.54.  Round 2 to decimal places.

obj = np.array([13,16,16,14,39])
A = np.zeros((2,5))
A[0,:] = [11,53,5,5,29] # time0
A[1,:] = [3,6,5,1,34] # time1
b = np.array([40,20]) # limits on time0 and time1
sense = np.array(['<','<'])

socModel = gp.Model()
socModX = socModel.addMVar(5,lb=[0,0,0,0,0],ub=[1,1,1,1,1])
socModCon = socModel.addMConstrs(A, socModX, sense, b)
socModel.setMObjective(None,obj,0,sense=gp.GRB.MAXIMIZE)

socModel.Params.OutputFlag = 0 # tell gurobi to shut up!!

socModel.optimize() # solve the LP
print("Max NPV is ${0:.2f}mn".format(socModel.objVal))
print("Star Oil Co. should invest {0:.0f}% in opportunity 3".format(socModX.x[2]*100))
