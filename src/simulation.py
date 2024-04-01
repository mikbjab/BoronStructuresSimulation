import random
import copy
from src.util import parametersHandling, viewGrid, fittingFunctions
from src.util.Grid import Grid


# creating mutation
def mutation(parent: Grid, num_of_modifications):
    red_positions = parent.grid[0]
    blue_positions = parent.grid[1]
    num_of_blues = len(blue_positions)
    num_of_reds = len(red_positions)
    mutations=random.randint(1,num_of_modifications)
    for i in range(mutations):
        index_r = random.randint(0, num_of_reds - 1)
        index_b = random.randint(0, num_of_blues - 1)
        current_red=red_positions[index_r]
        red_positions[index_r]=blue_positions[index_b]
        blue_positions[index_b]=current_red
    return Grid(parent.data,[red_positions, blue_positions])

def evolution_genetic(parent,num_of_steps,num_of_mutations):
    first_grid=copy.deepcopy(parent)
    population=[mutation(first_grid,num_of_mutations) for _ in range(20)]
    population.append(first_grid)
    population.sort(key=lambda grid: fittingFunctions.energy_with_table(grid.grid[0]))



def evolution(parent, num_of_steps, num_of_mutations):
    first = copy.deepcopy(parent)
    solv = [first]

    for i in range(num_of_steps):
        child = mutation(copy.deepcopy(parent), num_of_mutations)
        parent_energy = fittingFunctions.energy_with_table(parent.grid[0])
        child_energy = fittingFunctions.energy_with_table(child.grid[0])
        if child_energy >= parent_energy:
            parent = copy.deepcopy(child)
            solv.append(copy.deepcopy(parent))
            print(child_energy,i)
    return solv

def evolution_spring(parent, num_of_steps,num_of_mutations, filename):
    first = copy.deepcopy(parent)
    solv = [first]

    for i in range(num_of_steps):
        child = mutation(copy.deepcopy(parent), num_of_mutations)
        parent_energy = fittingFunctions.energy_spring_from_file(parent.grid[0], filename)
        child_energy = fittingFunctions.energy_spring_from_file(child.grid[0], filename)
        if child_energy >= parent_energy:
            parent = copy.deepcopy(child)
            solv.append(copy.deepcopy(parent))
            print(child_energy, i)
    return solv

if __name__=="__main__":
    data= parametersHandling.load_configuration("resources/parameters.json")
    l=data["size"]
    R=data["radius"]
    fps=data["steps"]
    num_of_mut=data["max_mut"]
    first_grid=Grid(data)
    first_grid.producing_red_blue_grid()
    print(len(first_grid.grid[0]))
    #solution = evolution_spring(first_grid, fps, num_of_mut, "resources/least_square.json")
    solution =evolution(first_grid,fps,num_of_mut)
    viewGrid.printing_dots(solution[0], "first",R)
    viewGrid.printing_dots(solution[-1], "last",R)

