# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 23:22:34 2021

@author: sahil
"""

import numpy as np
import gurobipy as gp

# Q5
#
# A trading company is looking for a way to 
# maximize profit per transportation of their 
# goods. The company has a train available 
# with 3 wagons. 
# • When stocking the wagons they can choose 
# between 4 types of cargo, each with its own 
# specifications. 
# • How much of each cargo type should be 
# loaded on which wagon in order to 
# maximize profit? 
# • The following constraints must be taken in 
# consideration
# – Weight capacity per train wagon
# – Volume capacity per train wagon
# – Limited availability per cargo type
#
#  | Train Wagon | Wt Cap (MT) | Vol Cap (m3) |
#  |     w1      |     10      |     5000     | 
#  |     w2      |      8      |     4000     |
#  |     w3      |     12      |     8000     |
#
#
#  | Cargo Type | Available (MT) | Volume per MT (m3) | Profit per MT ($) |
#  |     c1     |       18       |         400        |        2000       |
#  |     c2     |       10       |         300        |        2500       |
#  |     c3     |        5       |         200        |        5000       |
#  |     c4     |       20       |         500        |        3500       |


obj = np.array([2000,2500,5000,3500]*3)
A = np.zeros((10,12))
A[0,0:4] = 1 # wagon 1 wt cap
A[1,4:8] = 1 # wagon 2 wt cap
A[2,8:12] = 1 # wagon 3 wt cap
A[3,0:4] = [400,300,200,500] # wagon 1 vol cap
A[4,4:8] = [400,300,200,500] # wagon 2 vol cap
A[5,8:12] = [400,300,200,500] # wagon 3 vol cap
A[6:10,0:4] = np.diag(np.ones(4)) # cargo cap
A[6:10,4:8] = np.diag(np.ones(4)) # cargo cap
A[6:10,8:12] = np.diag(np.ones(4)) # cargo cap
b = np.array([10,8,12,5000,4000,8000,18,10,5,20]) # limits
sense = np.array(['<']*10)

trainModel = gp.Model()
trainModX = trainModel.addMVar(12, lb=np.zeros(12))
trainModCon = trainModel.addMConstrs(A, trainModX, sense, b)
trainModel.setMObjective(None,obj,0,sense=gp.GRB.MAXIMIZE)

trainModel.Params.OutputFlag = 0 # tell gurobi to shut up!!

trainModel.optimize() # solve the LP
print("Max Profit is ${0:.2f}".format(trainModel.objVal))
print(""""Load the cargo as follows:
      Wagon 1 - 
      \tC1: {0:.2f} MT
      \tC2: {1:.2f} MT
      \tC3: {2:.2f} MT
      \tC4: {3:.2f} MT
      Wagon 2 - 
      \tC1: {4:.2f} MT
      \tC2: {5:.2f} MT
      \tC3: {6:.2f} MT
      \tC4: {7:.2f} MT
      Wagon 3 - 
      \tC1: {8:.2f} MT
      \tC2: {9:.2f} MT
      \tC3: {10:.2f} MT
      \tC4: {11:.2f} MT""".format(trainModX.x[0],\
          trainModX.x[1],\
          trainModX.x[2],\
          trainModX.x[3],\
          trainModX.x[4],\
          trainModX.x[5],\
          trainModX.x[6],\
          trainModX.x[7],\
          trainModX.x[8],\
          trainModX.x[9],\
          trainModX.x[10],\
          trainModX.x[11]))

print("\n\nPrinting the train:")
print("""
      _<>_______    ______    ______   ______    ______    ______    ______    ______    ______    ______    ______    ______    ______        ___
      | |    | | =    {0:.0f}    =    {1:.0f}    =    {2:.0f}    =    {3:.0f}    =    {4:.0f}    =    {5:.0f}    =    {6:.0f}    =    {7:.0f}    =    {8:.0f}    =    {9:.0f}    =    {10:.0f}    =    {11:.0f}    =  _|___|_
     -----------   -------   -------   ------   ------    ------    ------    ------    ------    ------    ------    ------    ------       -------
      00     00     0   0     0   0    0   0    0   0     0   0      0   0    0   0     0   0     0   0     0   0     0   0     0   0         0  0
      """.format(trainModX.x[0],\
          trainModX.x[1],\
          trainModX.x[2],\
          trainModX.x[3],\
          trainModX.x[4],\
          trainModX.x[5],\
          trainModX.x[6],\
          trainModX.x[7],\
          trainModX.x[8],\
          trainModX.x[9],\
          trainModX.x[10],\
          trainModX.x[11]))
