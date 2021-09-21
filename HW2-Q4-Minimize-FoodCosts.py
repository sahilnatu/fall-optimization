# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 14:12:23 2021

@author: sahil
"""

import numpy as np
import gurobipy as gp

# Q4
#
# The goal of this problem is to select a set of foods that will satisfy a set
# of daily nutritional requirement at minimum cost. Suppose there are three foods
# available, corn, milk, and bread. There are restrictions on the number of calories
# (between 2000 and 2250) and the amount of Vitamin A (between 5000 and 50,000) that
# can be eaten. The table below shows, for each food, the cost per serving, the amount
# of Vitamin A per serving, and the number of calories per serving. Also, the maximum
# number of servings for each food is 10.
#
# How many servings of corn should you eat?  Round to 2 decimal places.

obj = np.array([0.18,0.23,0.05])
A = np.zeros((4,3))
A[0,:] = [107,500,0] # vit a min
A[1,:] = [107,500,0] # vit a max
A[2,:] = [72,121,65] # cal min
A[3,:] = [72,121,65] # cal max
b = np.array([5000,50000,2000,2250]) # limits on vit a and cal
sense = np.array(['>','<','>','<'])

foodModel = gp.Model()
foodModX = foodModel.addMVar(3,lb=[0,0,0],ub=[10,10,10])
foodModCon = foodModel.addMConstrs(A, foodModX, sense, b)
foodModel.setMObjective(None,obj,0,sense=gp.GRB.MINIMIZE)

foodModel.Params.OutputFlag = 0 # tell gurobi to shut up!!

foodModel.optimize() # solve the LP
print("Min Cost is ${0:.2f}".format(foodModel.objVal))
print("Servings of Corn: {0:.2f}".format(foodModX.x[0]))
