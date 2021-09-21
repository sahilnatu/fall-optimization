# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 23:22:34 2021

@author: sahil
"""

import numpy as np
import gurobipy as gp

# Q5
#
# Paper and wood products companies need to define cutting schedules that will
# maximize the total wood yield of their forests over some planning period.
# Suppose that a firm with control of 2 forest units wants to identify the
# best cutting schedule over a planning horizon of 3 years. Forest unit 1 has
# a total acreage of 2 and unit 2 has a total of 3 acres. The studies that the
# company has undertaken predict that each acre in unit 1(2) will have
# 1, 1.3, 1.4 (1, 1.2, 1.6) tons of woods per acre available for harvesting
# in year 1, 2, 3 respectively. Based on its prediction of economic conditions,
# the company believes that it should harvest at least 1.2, 1.5, 2 tons of
# wood in year 1, 2, 3 separately. Due to the availability of equipment and
# personnel, the company can harvest at most 2, 2, 3 tons of wood in
# year 1, 2, 3. Find the company’s best cutting strategy that maximizes the
# total weights of wood. Here discounting of the time value should not be
# considered.  If some fraction of a forest unit is cut down in year 1, that
# part of the forest cannot be cut again for the remaining 2 years.  Similarly
# if some fraction of the forest unit is cut down in year 2 it cannot be cut
# in year 3.
#
# In year 3, how many acres of forest unit 2 should be cut down?  Round to
# 2 decimal places.

obj = np.array([1,1,1,1,1,1])
A = np.zeros((12,6))
A[0,:] = [1,0,0,0,0,0] # forest 1 year 1
A[1,:] = [-1,1,0,0,0,0] # forest 1 year 2
A[2,:] = [-1,-1,1,0,0,0] # forest 1 year 3
A[3,:] = [0,0,0,1,0,0] # forest 2 year 1
A[4,:] = [0,0,0,-1,1,0] # forest 2 year 2
A[5,:] = [0,0,0,-1,-1,1] # forest 2 year 3
A[6,:] = [1,0,0,1,0,0] # economic condition year 1
A[7,:] = [0,1,0,0,1,0] # economic condition year 2
A[8,:] = [0,0,1,0,0,1] # economic condition year 3
A[9,:] = [1,0,0,1,0,0] # labor constraint year 1
A[10,:] = [0,1,0,0,1,0] # labor constraint year 2
A[11,:] = [0,0,1,0,0,1] # labor constraint year 3
b = np.array([2,2.6,2.8,3,3.6,4.8,1.2,1.5,2,2,2,3]) # limits
sense = np.array(['<','<','<','<','<','<','>','>','>','<','<','<'])

woodModel = gp.Model()
woodModX = woodModel.addMVar(6)
woodModCon = woodModel.addMConstrs(A, woodModX, sense, b)
woodModel.setMObjective(None,obj,0,sense=gp.GRB.MAXIMIZE)

woodModel.Params.OutputFlag = 0 # tell gurobi to shut up!!

woodModel.optimize() # solve the LP
print("Max Wood Yield is {0:.2f} MT".format(woodModel.objVal))
print("Acres of Forest Unit 2 Cut in Year 3: {0:.2f}".format(woodModX.x[5]/1.6))
