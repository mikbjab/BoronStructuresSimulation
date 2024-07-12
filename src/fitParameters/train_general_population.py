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
num_of_training_steps = 10
training_dir = "../../resources/training_big/"
train_with_random=True
current_model=models.model_spring
parameters_sign = [1, 1, -1]
population_size=10
steps_per_population=3
num_parents_survival=3
parameters_population = []  # if given here, then they will not be generated randomly
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
    if not len(parameters_population)>0:
        for _ in range(population_size):
            temp=[]
            for sign in parameters_sign:
                temp.append(random.uniform(0.1,0.8)*sign)
            parameters_population.append(temp)
    counter=0

    guess_check=[parameters_population]
    parent_population = copy.deepcopy(parameters_population)
    parent_MSE = [(parent, MSE_general(parent, training_grids, current_model)) for parent in parent_population]
    initial_MSE=copy.deepcopy(parent_MSE)
    print("Initial: ")
    for parent in initial_MSE:
        print(parent)

    while True:
        child_population=[]
        for parent in parent_MSE:
            child_temp=parent[0]
            for _ in range(steps_per_population):
                while True:
                    child = change_guess(child_temp, uniform=True)
                    child_MSE = MSE_general(child, training_grids, current_model)
                    if child_MSE < parent_MSE[parent_MSE.index(parent)][1]:
                        child_temp=child
                        break
            child_population.append((child_temp,child_MSE))

        parent_MSE = sorted(parent_MSE, key=lambda x: x[1])[:num_parents_survival]
        parent_MSE.extend(sorted(child_population,key=lambda x:x[1])[:population_size-num_parents_survival])

        counter+=1
        guess_check.append(parent_MSE)
        print(counter)
        for parent in parent_MSE:
            print(parent)

        if counter > num_previous_step and counter > num_of_training_steps:
            previous_min_MSE = min(guess_check[-num_previous_step],key=lambda x:x[1])
            current_min_MSE=min(parent_MSE,key=lambda x:x[1])
            if (previous_min_MSE - current_min_MSE) / previous_min_MSE < change:
                break



    print("Final: "," steps: ", counter)
    for parent in parent_MSE:
        print(parent)



