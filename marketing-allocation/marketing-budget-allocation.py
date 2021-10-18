# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 18:17:16 2021

@author: sahil
"""

import pandas as pd
import numpy as np
import gurobipy as gp

roi_df = pd.read_csv(r'ROI_data.csv')
roi_df.set_index('Platform',inplace=True)

def optimize_allocation(df,estimate,budget,constraint_3=True):
    """
    

    Parameters
    ----------
    df : Dataframe
        ROI dataframe to be used
    estimate : integer
        ROI estimate to be used
    budget : integer
        Total company budget for marketing

    Returns
    -------
    list
        List comprising of maximum returns and allocations for different marketing mediums

    """
    obj = np.array(df.iloc[estimate,:])
    A = np.zeros((3,df.shape[1]))
    A[0,:] = 1
    for column in df.columns:
        if column == 'Print':
            A[1,df.columns.get_loc(column)] = 1
        if column == 'TV':
            A[1,df.columns.get_loc(column)] = 1
        if column == 'SEO':
            A[2,df.columns.get_loc(column)] = -2
        if column == 'AdWords':
            A[2,df.columns.get_loc(column)] = -2
        if column == 'Facebook':
            A[1,df.columns.get_loc(column)] = -1
            A[2,df.columns.get_loc(column)] = 1
        if column == 'LinkedIn':
            A[2,df.columns.get_loc(column)] = 1
        if column == 'Instagram':
            A[2,df.columns.get_loc(column)] = 1
        if column == 'Snapchat':
            A[2,df.columns.get_loc(column)] = 1
        if column == 'Twitter':
            A[2,df.columns.get_loc(column)] = 1
        if column == 'Email':
            A[1,df.columns.get_loc(column)] = -1
    b = np.array([budget,0,0])
    sense = np.array(['<','<','>'])

    budgetModel = gp.Model()
    ub_constraint = np.ones(10)*3000000
    if constraint_3 == False:
        ub_constraint = np.ones(10)*budget
    budgetModX = budgetModel.addMVar(df.shape[1], lb=np.zeros(10), ub=ub_constraint)
    budgetModCon = budgetModel.addMConstr(A, budgetModX, sense, b)
    budgetModel.setMObjective(None,obj,0,sense=gp.GRB.MAXIMIZE)

    budgetModel.Params.OutputFlag = 0 # tell gurobi to shut up!!

    budgetModel.optimize() # solve the LP
    #print("Max Returns is ${0:.2f}\n".format(budgetModel.objVal))
    #print("Allocation Strategy is as follows:")
    #for column in roi_df.columns:
        #print("{0}: ${1:.2f}".format(column,budgetModX.x[roi_df.columns.get_loc(column)]))
    
    constraints_sensitivity = np.zeros((3,3))
    constraints_sensitivity[:,0] = [con.Pi for con in budgetModCon]
    constraints_sensitivity[:,1] = [con.SARHSLow for con in budgetModCon]
    constraints_sensitivity[:,2] = [con.SARHSUp for con in budgetModCon]
    obj_sensitivity = np.zeros((df.shape[1],3))
    obj_sensitivity[:,0] = budgetModX.SAObjLow
    obj_sensitivity[:,2] = budgetModX.SAObjUp
    obj_sensitivity[:,1] = obj
    obj_sensitivity = obj_sensitivity.T

    return [budgetModel.objVal, budgetModX.x, constraints_sensitivity, obj_sensitivity]
        
total_budget_original = 10000000

"""
Q1 - Q4
Finding optimized budget allocations based on ROI estimates from both companies
"""
max_returns, allocations, constraints, obj_sensitivity = optimize_allocation(roi_df,0,total_budget_original)
max_returns_2, allocations_2, constraints_2, obj_sensitivity_2 = optimize_allocation(roi_df,1,total_budget_original)

"""
Q5
Returns achieved if 1st ROI Data is correct and we allocate based on 2nd ROI Data
"""
returns_1_2 = np.matmul(allocations_2.T,np.array(roi_df.iloc[0,:]))
returns_loss_1_2 = max_returns - returns_1_2
"""
Q5
Returns achieved if 2nd ROI Data is correct and we allocate based on 1st ROI Data
"""
returns_2_1 = np.matmul(allocations.T,np.array(roi_df.iloc[1,:]))
returns_loss_2_1 = max_returns_2 - returns_2_1

"""
Q5
Removing the 3rd constraint, we try calculating the loss in returns as done above
"""
max_returns_no3constraint, allocations_no3constraint, constraints_no3constraint, obj_sensitivity_no3constraint = optimize_allocation(roi_df,0,total_budget_original,constraint_3=False)
max_returns_2_no3constraint, allocations_2_no3constraint, constraints_2_no3constraint, obj_sensitivity_2_no3constraint = optimize_allocation(roi_df,1,total_budget_original,constraint_3=False)
returns_1_2_no3constraint = np.matmul(allocations_2_no3constraint.T,np.array(roi_df.iloc[0,:]))
returns_loss_1_2_no3constraint = max_returns_no3constraint - returns_1_2_no3constraint
returns_2_1_no3constraint = np.matmul(allocations_no3constraint.T,np.array(roi_df.iloc[1,:]))
returns_loss_2_1_no3constraint = max_returns_2_no3constraint - returns_2_1_no3constraint
"""
With the 3rd constraint removed, we allocate far higher sums to a single marketing medium, thereby making
our strategy a lot more risky. As it turns out, putting all the eggs in the same basket is not
the best strategy, and there is a greater loss of returns if the ROI estimates are wrong as compared
to when we had the 3rd constraint in place.
"""

"""
Q6
Sensitivity analysis
"""
print("-"*30)
print("The ROI estimates can be wiggled as follows without changing the allocation strategy:")
for column in roi_df.columns:
    print("{0}: Between {1:.2f}% and {2:.2f}%".format(column, obj_sensitivity[0,roi_df.columns.get_loc(column)]*100, obj_sensitivity[2,roi_df.columns.get_loc(column)]*100))
print("-"*30)
"""
Monthly problem
"""
roi_mo_df = pd.read_csv(r'roi_mat.csv')
roi_mo_df.set_index('Unnamed: 0',inplace=True)
roi_mo_df = roi_mo_df.apply(lambda x: x/100)

returns_earned = 0
max_returns_monthly = np.zeros(12)
allocations_monthly = np.zeros((12,roi_df.shape[1]))
for i in range(12):
    budget = total_budget_original + returns_earned*0.5
    max_returns_monthly[i], allocations_monthly[i], constraints_monthly, obj_sensitivity_monthly = optimize_allocation(roi_mo_df,i,budget)
    returns_earned += max_returns_monthly[i]
# Optimal allocation for each month is each row of allocations_monthly

max_monthly_allocation_change = np.zeros(roi_mo_df.shape[1])
for j in range(allocations_monthly.shape[1]):
    delta = 0
    for i in range(allocations_monthly.shape[0]-1):
        if allocations_monthly[i+1,j]-allocations_monthly[i,j]>delta:
            delta = allocations_monthly[i+1,j]-allocations_monthly[i,j]
    max_monthly_allocation_change[j] = delta

if max(max_monthly_allocation_change/1000000)>1:
    print('Since max of max_monthly_allocation_change is over $1mn, budget is unstable')
    print('In order to get a stable budget, we have to add additional constraints such that difference between allocation to a particular medium in a particular month and the allocation to the same medium in the previous month is under $1 million')
    print('-'*30)
else:
    print('Since max of max_monthly_allocation_change is under $1mn, budget is stable')
    print('-'*30)