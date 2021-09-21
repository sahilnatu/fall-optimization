# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 09:58:32 2021

@author: sahil
"""

import numpy as np
import gurobipy as gp
import pandas as pd
import matplotlib as plt

# Q2
# A farmer in Iowa owns 450 acres of land. He is going to plant each acre with 
# wheat or corn. Each acre planted with wheat (corn) yields $2,000 ($3,000) profit,
# requires three (two) workers, and requires two (four) tons of fertilizer.
# There are currently 1,000 workers and 1,200 tons of fertilizer available.

obj = np.array([2000,3000]) # objective vector
A = np.zeros((3,2)) # initialize constraint matrix
A[0,:] = [1,1] # area constraint
A[1,:] = [3,2] # workers constraint
A[2,:] = [2,4] # fertilizer constraint
b = np.array([450,1000,1200]) # limits on area, workers, fertilizer
sense = np.array(['<','<','<']) # all constraints are less than or equal constraints

farmModel = gp.Model() # initialize an empty model
farmModX = farmModel.addMVar(2) # tell the model how many variables there are
# must define the variables before adding constraints because variables go into the constraints
farmModCon = farmModel.addMConstrs(A, farmModX, sense, b) # add the constraints to the model
farmModel.setMObjective(None,obj,0,sense=gp.GRB.MAXIMIZE) # add the objective to the model

farmModel.Params.OutputFlag = 0 # tell gurobi to shut up!!

farmModel.optimize() # solve the LP
print("Max Profit is ${0:.2f}".format(farmModel.objVal)) # optimal revenue level
print("Wheat acres: {0:.2f}\nCorn acres: {1:.2f}".format(farmModX.x[0],farmModX.x[1])) # values of coeff of X

farmModelDF = pd.DataFrame(columns=['fertilizer_qty','wheat_qty','corn_qty'])
fertilizer_amounts = [200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200]
for amount in fertilizer_amounts:
    obj_2 = np.array([2000,3000])
    A_2 = np.zeros((3,2))
    A_2[0,:] = [1,1]
    A_2[1,:] = [3,2]
    A_2[2,:] = [2,4]
    b_2 = np.array([450,1000,amount])
    sense_2 = np.array(['<','<','<'])

    farmModel_2 = gp.Model()
    farmModX_2 = farmModel_2.addMVar(2)
    farmModCon_2 = farmModel_2.addMConstrs(A_2, farmModX_2, sense_2, b_2)
    farmModel_2.setMObjective(None,obj_2,0,sense=gp.GRB.MAXIMIZE)

    farmModel_2.Params.OutputFlag = 0

    farmModel_2.optimize()
    farmModelDF = farmModelDF.append(pd.DataFrame([[amount,farmModX_2.x[0],farmModX_2.x[1]]],columns=(['fertilizer_qty','wheat_qty','corn_qty'])),ignore_index=True)
    print("For Fertilizer Qty of {0:.0f} MT".format(amount))
    print("Max Profit is ${0:.2f}".format(farmModel_2.objVal))
    print("Wheat acres: {0:.2f}\nCorn acres: {1:.2f}".format(farmModX_2.x[0],farmModX_2.x[1]))
    print("-"*30)
    
plt.pyplot.figure(1)
plt.pyplot.bar(farmModelDF.astype({'fertilizer_qty':str})['fertilizer_qty'],farmModelDF['wheat_qty'])