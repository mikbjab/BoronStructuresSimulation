import copy
import json
import random

from src.util.generate_structures import generate_structures
import src.util.GridFactory as GridFactory
import src.util.fittingFunctions as fitFun


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

def random_walk(init_guess,steps,training_set,uniform=True):
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






