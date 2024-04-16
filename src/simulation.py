import math
import random
import copy

from src import analysis
from src.util import parametersHandling, viewGrid, fittingFunctions
from src.util.Grid import Grid
import src.util.GridFactory as GridFactory


# creating mutation
def mutation(parent: Grid, num_of_modifications, variance=4):
    red_positions = parent.grid[0]
    blue_positions = parent.grid[1]
    num_of_blues = len(blue_positions)
    num_of_reds = len(red_positions)
    random.seed()
    mutations=random.randint(1,num_of_modifications)
    for i in range(mutations):
        random.seed()
        index_r = random.randint(0, num_of_reds - 1)
        random.seed()
        index_b = random.randint(0, num_of_blues - 1)
        current_red=red_positions[index_r]
        red_positions[index_r]=blue_positions[index_b]
        blue_positions[index_b]=current_red
    return Grid({"size":parent.l,"radius":parent.R},[red_positions, blue_positions])

def evolution_genetic(parent,num_of_steps,num_of_mutations):
    first_grid=copy.deepcopy(parent)
    population=[mutation(first_grid,num_of_mutations) for _ in range(20)]
    population.append(first_grid)
    population.sort(key=lambda grid: fittingFunctions.energy_with_table(grid.grid[0]))



def evolution(parent, num_of_steps, num_of_mutations):
    parent_energy=0
    i=0
    while i<num_of_steps or parent_energy<6.1:
        child = mutation(copy.deepcopy(parent), num_of_mutations)
        parent_energy = fittingFunctions.energy_with_table(parent.grid[0])
        child_energy = fittingFunctions.energy_with_table(child.grid[0])
        if child_energy >= parent_energy:
            parent = copy.deepcopy(child)
            print(parent_energy,i)
        i+=1

    return parent

def evolution_spring(parent, num_of_steps,num_of_mutations, filename):
    first = copy.deepcopy(parent)
    solv = [first]

    for i in range(num_of_steps):
        child = mutation(copy.deepcopy(parent), num_of_mutations)
        parent_energy = fittingFunctions.energy_spring_from_param(parent.grid[0], filename)
        child_energy = fittingFunctions.energy_spring_from_param(child.grid[0], filename)
        if child_energy >= parent_energy:
            parent = copy.deepcopy(child)
            solv.append(copy.deepcopy(parent))
            print(child_energy, i)
    return solv

def evolution_population(parent, num_of_steps, num_of_swap, population_size,model):
    first = copy.deepcopy(parent)
    population=[]
    for i in range(population_size-1):
        population.append(mutation(copy.deepcopy(first), num_of_swap//2))
        viewGrid.printing_dots(population[i],f"{i}",i)
    population.append(first)

    counter=0
    while counter<num_of_steps:
        print(counter)
        population.sort(key=lambda x:model(x.grid[0]),reverse=True)
        best_candidate=population[0]
        print(fittingFunctions.energy_with_table(best_candidate.grid[0]))
        second_best_candidate=population[1]
        worst_candidate=population[-1]
        temp=(population_size-3)//3
        population=[best_candidate, second_best_candidate, worst_candidate]
        for i in range(temp):
            population.append(mutation(best_candidate,num_of_swap))
            population.append(mutation(second_best_candidate,num_of_swap))
      
        for i in range(population_size-2*temp-3):
            population.append(mutation(worst_candidate, num_of_swap))
        counter+=1
    return population





if __name__=="__main__":
    data= parametersHandling.load_configuration("resources/parameters.json")
    l=data["size"]
    R=data["radius"]
    fps=data["steps"]
    num_of_mut=data["max_mut"]
    first_grid=GridFactory.create_from_json("resources/parameters.json")
    first_grid=GridFactory.create_random_gridObject(15,"uniform",0.3, 0.3)
    #solution = evolution_spring(first_grid, fps, num_of_mut, [0.13442410124025683, 1.1100909554658314, 0.004773775067342759])
    solution =evolution(first_grid,fps,num_of_mut)
    viewGrid.printing_dots(first_grid, "first",R)
    viewGrid.printing_dots(solution, "last",R)
    print("initial ratio: ",analysis.calculate_ratio(first_grid))
    print("initial ratio: ",analysis.calculate_ratio(solution))
    # solv_population=evolution_population(first_grid,1000,4,30,fittingFunctions.energy_with_table)
    # for i in range(30):
    #     viewGrid.printing_dots(solv_population[i],f"{i}, {fittingFunctions.energy_with_table(solv_population[i].grid[0])}",0)

