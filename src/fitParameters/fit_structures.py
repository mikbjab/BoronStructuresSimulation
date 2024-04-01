import copy
import json
import random
import src.util.Grid as G
import numpy as np
from src.util.GridFactory import GridFactory
from src.util.viewGrid import printing_dots
import src.util.fittingFunctions as fitFun
from src.simulation import evolution


def generate_structures(n,directory,num_steps=30000,num_mut=3):
    for i in range(n):
        s = int(random.uniform(4, 9))
        R = random.uniform(0.5 * s, 0.7 * s)
        N_blue = int(np.pi * R * R * random.uniform(0.1, 0.3))
        temp_data={"size":s,"radius":R,"number_blue":N_blue}
        grid=G.Grid(temp_data)
        GridFactory.produce_default_red_grid(grid)
        GridFactory.remove_outside_dots(grid)
        GridFactory.add_random_blue_dots(grid)
        printing_dots(grid,str(i),1)
        temp_grid=evolution(grid,num_steps,num_mut)[-1]
        printing_dots(temp_grid,str(i),1)
        GridFactory.save_grid(temp_grid,f"../resources/{directory}/grid{i}.json")

def MSE(guess,training_set):
    result=0
    for grid in training_set:
        result+= (fitFun.energy_with_table(grid.grid[0]) - fitFun.energy_k(fitFun.parameters_count(grid.grid[0]), guess[0], guess[1], guess[2])) ** 2
    return result/len(training_set)

def mutate(guess, custom_variance=1,uniform=False):
    while True:
        if uniform:
            rate = random.uniform(0, 0.3)
        else:
            rate = random.gauss(0, 0.15 * custom_variance)
        i = random.randint(0, 2)
        new_guess = copy.deepcopy(guess)
        new_guess[i] += rate * new_guess[i]
        #if new_guess[1] > new_guess[0] > new_guess[2]:
        return new_guess

def mutate_population(guess,num_of_members):
    result=[]
    for i in range(num_of_members-num_of_members//3):
        result.append(mutate(guess[0]))
    for i in range(num_of_members//3):
        result.append(mutate(guess[1],2))
    return result

def choose_best(population,training_set):
    population.sort(key=lambda member:MSE(member,training_set))
    return [population[0],population[-1]]

def genetic_algorithm(initial_population,num_of_members,steps,training_set):
    nucleus=initial_population
    for i in range(steps):
        print(i)
        population=mutate_population(nucleus,num_of_members)
        nucleus=choose_best(population,training_set)
    return nucleus

def random_walk(init_guess,steps,training_set,uniform=False):
    parent_guess=copy.deepcopy(init_guess)
    for i in range(steps):
        parent_MSE=MSE(parent_guess,training_set)
        print(i, parent_MSE, parent_guess)
        while True:
            child_guess=mutate(parent_guess,uniform=uniform)
            child_MSE=MSE(child_guess,training_set)
            if child_MSE<parent_MSE:
                parent_guess=child_guess
                break
    return parent_guess



if __name__=="__main__":
    num_of_training_structures=10
    num_of_training_steps=300
    num_of_population_members=20
    generate_structures(num_of_training_structures,"training_evolved")
    training_grids=[]
    for indexx in range(num_of_training_structures):
        training_grids.append(GridFactory.create_from_json(f"../resources/training_evolved/grid{indexx}.json"))

    k2=random.uniform(0.5,1)
    k1=random.uniform(0.0001,k2)
    k3=random.uniform(0.0001,k1)
    initial_guess=[k1,k2,k3]

    k2=random.uniform(0.5,1)
    k1=random.uniform(0.0001,k2)
    k3=random.uniform(0.0001,k1)
    second_guess=[k1,k2,k3]
    first_population=[initial_guess,second_guess]
    print(initial_guess, MSE(initial_guess,training_grids))
    #[initial_guess,second_guess]=genetic_algorithm(first_population,num_of_population_members,num_of_training_steps,training_grids)
    initial_guess=random_walk(initial_guess,num_of_training_steps,training_grids)
    print("final: ",initial_guess,MSE(initial_guess,training_grids))

    with open("../resources/fit_parameters.json", "w") as file:
        json.dump({"k1":initial_guess[0],"k2":initial_guess[1],"k3":initial_guess[2]},file)






