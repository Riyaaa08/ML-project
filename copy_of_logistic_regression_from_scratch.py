# -*- coding: utf-8 -*-
"""Copy of Logistic_Regression_from_scratch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Sh65KtRatI_nq3Ftf1YWC7FsBSGqvvan
"""

import csv 
import numpy as np 
import matplotlib.pyplot as plt 
  
# step 1 : Load CSV file
def loadCSV(filename): 
    ''' 
    function to load dataset 
    '''
    with open(filename,"r") as csvfile: 
        lines = csv.reader(csvfile) 
        dataset = list(lines) 
        for i in range(len(dataset)): 
            dataset[i] = [float(x) for x in dataset[i]]      
    return np.array(dataset) 
  
  # step 2 : Normalize 
def normalize(X): 
    ''' 
    function to normalize feature matrix, X 
    '''
    mins = np.min(X, axis = 0) 
    maxs = np.max(X, axis = 0) 
    rng = maxs - mins 
    norm_X = 1 - ((maxs - X)/rng) 
    return norm_X 
  
  # step 3 :  
def logistic_func(beta, X): 
    ''' 
    logistic(sigmoid) function 
    '''
    # below is the code for 1/1+e^(-(bo*x1+ b1*x2 +  b1*x3............ ))
    return 1.0/(1 + np.exp(-np.dot(X, beta.T))) 
  
  
def log_gradient(beta, X, y): 
    ''' 
    logistic gradient function 
    '''
    #first_calc = y_prediction - y_actual  for all samples 
    first_calc = logistic_func(beta, X) - y.reshape(X.shape[0], -1) 
    # now in below step we will find the partial derivative
    #final_calc= gradient is (y_prediction - y_actual)*x  for all samples 
    final_calc = np.dot(first_calc.T, X) 
    
    return final_calc 
  
  
def cost_func(beta, X, y): 
    ''' 
    cost function, J 
    '''
    #y_prediction=  1/1+e^(-(bo*x1+ b1*x2 +  b1*x3............ )) for all samples
    y_prediction= logistic_func(beta, X) 
    y = np.squeeze(y) 
    # calculate cross entropy cost function for all samples
    cost_function = -(y * np.log(y_prediction)) - ((1 - y) * np.log(1 - y_prediction) ) 
    # return the sum of  cost function divided by no. of samples
    return np.mean(cost_function) 
  
  
def train(X, y, beta, lr=.01, converge_change=.001): 
    ''' 
    gradient descent function 
    '''
    cost = cost_func(beta, X, y) 
    change_cost = 1
    num_iter = 1
      
    while(change_cost > converge_change): 
        old_cost = cost 
        #beta= beta - learning_rate * partial derivative of cost function w.r.t beta
        beta = beta - (lr * log_gradient(beta, X, y)) 
        # again calculate cost function
        cost = cost_func(beta, X, y) 
        # find difference between old cost and new cost 
        #if change is greater than .001 then reiterate 
        change_cost = old_cost - cost 
        num_iter += 1
      
    return beta, num_iter  
  
  
def pred_values(beta, X): 
    ''' 
    function to predict labels 
    '''
    pred_prob = logistic_func(beta, X) 
    pred_value = np.where(pred_prob >= .5, 1, 0) 
    return np.squeeze(pred_value) 
  
  
def plot_reg(X, y, beta): 
    ''' 
    function to plot decision boundary 
    '''
    # labelled observations 
    x_0 = X[np.where(y == 0.0)] 
    x_1 = X[np.where(y == 1.0)] 
      
    # plotting points with diff color for diff label 
    plt.scatter([x_0[:, 1]], [x_0[:, 2]], c='b', label='y = 0') 
    plt.scatter([x_1[:, 1]], [x_1[:, 2]], c='r', label='y = 1') 
      
    # plotting decision boundary 
    x1 = np.arange(0, 1, 0.1) 
    x2 = -(beta[0,0] + beta[0,1]*x1)/beta[0,2] 
    plt.plot(x1, x2, c='k', label='reg line') 
  
    plt.xlabel('x1') 
    plt.ylabel('x2') 
    plt.legend() 
    plt.show() 
      
  
      
if __name__ == "__main__": 
    # load the dataset 
    dataset = loadCSV('/content/dataset1.csv') 
      
    # normalizing feature matrix 
    X = normalize(dataset[:, :-1]) 
    print(X)
      
    # stacking columns wth all ones in feature matrix 
    X = np.hstack((np.matrix(np.ones(X.shape[0])).T, X))
    print(X)
  
    # response vector 
    y = dataset[:, -1] 
  
    # initial beta values 
    beta = np.matrix(np.zeros(X.shape[1])) 
  
    # beta values after running gradient descent 
    beta, num_iter =train(X, y, beta) 
  
    # estimated beta values and number of iterations 
    print("Estimated regression coefficients:", beta) 
    print("No. of iterations:", num_iter) 
  
    # predicted labels 
    y_pred = pred_values(beta, X) 
      
    # number of correctly predicted labels 
    print("Correctly predicted labels:", np.sum(y == y_pred)) 
      
    # plotting regression line 
    plot_reg(X, y, beta)

