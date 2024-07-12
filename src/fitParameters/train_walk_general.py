import copy
import os
import random

import numpy as np

from src.util import models
from src.util import GridFactory as GF

def MSE_general(guess,training_set,model):
    result=0
    for grid in training_set:
        result+= (models.model_table(grid) - model(grid, guess)) ** 2
    return result/len(training_set)

def change_guess(guess, custom_variance=0.5,uniform=False):
    rate=[]
    if uniform:
        rate=[random.uniform(-0.3,0.3) for _ in range(num_param)]
    else:
        rate = [random.gauss(0, 0.15 * custom_variance) for _ in range(num_param)]
    choices = np.random.choice(num_param,size=num_param_change)
    new_guess = copy.deepcopy(guess)
    for choice in choices:
        new_guess[choice]+=rate[choice] *new_guess[choice]
    return new_guess

# parameters for training:
num_of_training_steps = 50
training_dir = "../../resources/training_big/"
train_with_random=True
current_model=models.model_anisotropic
parameters_sign = [-1, 1, 1]
parameters = []  # if given here, then they will not be generated randomly
num_param_change = 3  # must be <= len(parameters_sign)
num_param=len(parameters_sign)

# for ending the training loop, the loop will end if the relative change between
# [last] parameters and [last-num_previous_step] parameters will be < change
num_previous_step = 5
change = 0.01

if __name__=="__main__":
    # loading training set
    fileNames=os.listdir(training_dir)
    training_grids=[]
    energies=[]
    ratios=[]
    for fileName in fileNames:
        if "M5r" in fileName:
            temp=GF.create_from_json(training_dir+fileName)
            training_grids.append(temp)
        elif "init" in fileName:
            temp = GF.create_from_json(training_dir + fileName)
            training_grids.append(temp)


    # generating random parameters (if not given)
    if not len(parameters)>0:
        for sign in parameters_sign:
            parameters.append(random.uniform(0.1,0.8)*sign)

    counter=0
    guess_check=[parameters]
    parent_guess = copy.deepcopy(parameters)
    while True:
        parent_MSE = MSE_general(parent_guess, training_grids,current_model)
        while True:
            child_guess=change_guess(parent_guess,uniform=True)
            child_MSE=MSE_general(child_guess,training_grids,current_model)
            if child_MSE<parent_MSE:
                parent_guess=child_guess
                break
        counter+=1
        print(counter,child_MSE,child_guess)
        guess_check.append(child_guess)
        if counter>num_previous_step and counter>num_of_training_steps:
            previous_MSE=MSE_general(guess_check[-num_previous_step],training_grids,current_model)
            if (previous_MSE-child_MSE)/previous_MSE<change:
                break

    print("Initial: ",parameters,MSE_general(parameters,training_grids,current_model))
    print("Final: ",child_guess,child_MSE, "\n steps: ", counter)



