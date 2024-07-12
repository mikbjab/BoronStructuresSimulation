import random
import copy

from src.util import parametersHandling, viewGrid, analysis, models
from src.deprecated import fittingFunctions
from src.util.Grid import Grid
import src.util.GridFactory as GridFactory


# creating mutation
def mutation(parent: Grid, num_of_modifications):
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



def evolution(parent, num_of_steps, num_of_mutations,model=models.model_table,param=[],energy_condition=True):
    parent_energy=0
    i=0
    param_flag=False
    if model is not models.model_table:
        param_flag=True

    while i<num_of_steps or (energy_condition and parent_energy<6.1):
        child = mutation(copy.deepcopy(parent), num_of_mutations)
        if param_flag:
            parent_energy = model(parent,param)
            child_energy = model(child,param)
        else:
            parent_energy=model(parent)
            child_energy=model(child)
        if child_energy >= parent_energy:
            parent = copy.deepcopy(child)
            print(parent_energy,i)
        i+=1

    return parent

def evolution_spring(parent, num_of_steps,num_of_mutations, filename):
    first = copy.deepcopy(parent)

    for i in range(num_of_steps):
        child = mutation(copy.deepcopy(parent), num_of_mutations)
        parent_energy = fittingFunctions.energy_spring_from_param(parent.grid[0], filename)
        child_energy = fittingFunctions.energy_spring_from_param(child.grid[0], filename)
        if child_energy >= parent_energy:
            parent = copy.deepcopy(child)
            print(child_energy, i)
    return parent



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

def simulate_anisotropic(parent,num_of_steps,num_of_swap, coeff_matrix):
    for i in range(num_of_steps):
        child = mutation(copy.deepcopy(parent), num_of_swap)
        parent_energy = fittingFunctions.anisotropic_model(parent, coeff_matrix)
        child_energy = fittingFunctions.anisotropic_model(child, coeff_matrix)
        if child_energy >= parent_energy:
            parent = copy.deepcopy(child)
            print(child_energy, i)
    return parent

def simulate_clusters(parent,num_of_steps,num_of_swap, coefficients):
    for i in range(num_of_steps):
        child = mutation(copy.deepcopy(parent), num_of_swap)
        parent_energy = fittingFunctions.clusters_model_basic(parent, coefficients)
        child_energy = fittingFunctions.clusters_model_basic(child, coefficients)
        if child_energy >= parent_energy:
            parent = copy.deepcopy(child)
            print(child_energy, i)
    return parent


def weird_simulate_clusters(parent,num_of_steps,num_of_swap, coefficients):
    for i in range(num_of_steps):
        child = mutation(copy.deepcopy(parent), num_of_swap)
        parent_energy = fittingFunctions.clusters_model_basic(parent, coefficients)
        child_energy = fittingFunctions.clusters_model_basic(child, coefficients)
        if abs(child_energy-6.53)<abs(parent_energy-6.53):
            parent = copy.deepcopy(child)
            print(child_energy, i)
    return parent


if __name__=="__main__":
    data= parametersHandling.load_configuration("../resources/parameters.json")
    l=data["size"]
    R=data["radius"]
    fps=100000
    num_of_mut=data["max_mut"]
    first_grid=GridFactory.create_from_json("test_grid.json")
    viewGrid.printing_dots(first_grid, "test grid ",R)
    solution = evolution(first_grid, fps, num_of_mut
                         ,model=models.model_spring
                         ,param=[-0.475234201367123, 2.046648324829256, -0.01679292882896216]
                         ,energy_condition=False)
    #[0.213803468494253, 0.5826535997946278, 0.09733891086066418] 0.2 MSE
    #[0.009738352045112635, 1.3621416202976369, 0.00024772030574858465] 0.053029140859907384
    #solution1 =evolution(first_grid,fps,num_of_mut)
    viewGrid.printing_dots(solution, "spring first",R)
    viewGrid.save_grid(solution,"spring-++","spring-++.jpg")
    #viewGrid.printing_dots(solution1, "initial model",R)
    print("initial ratio: ", analysis.calculate_ratio(first_grid))
    print("final ratio: ", analysis.calculate_ratio(solution))
    # solv_population=evolution_population(first_grid,1000,4,30,fittingFunctions.energy_with_table)
    # for i in range(30):
    #     viewGrid.printing_dots(solv_population[i],f"{i}, {fittingFunctions.energy_with_table(solv_population[i].grid[0])}",0)

