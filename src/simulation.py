import random
import copy
from util import parametersHandling, viewGrid, fittingFunctions
from util.Grid import Grid


# creating mutation
def mutation(parent, num_of_modifications):
    temp_red = parent.grid[0]
    temp_blue = parent.grid[1]
    num_of_blues = len(temp_blue)
    num_of_reds = len(temp_red)
    mutations=random.randint(1,num_of_modifications)
    for i in range(mutations):
        index_b = random.randint(0, num_of_blues - 1)
        index_r = random.randint(0, num_of_reds - 1)
        temp = temp_blue[index_b]
        temp_blue[index_b] = temp_red[index_r]
        temp_red[index_r] = temp
    return Grid(parent.data,[temp_red, temp_blue])


def evolution(parent, num_of_steps, num_of_mutations):
    first = copy.deepcopy(parent)
    solv = [first]

    for i in range(num_of_steps):
        child = mutation(copy.deepcopy(parent), num_of_mutations)
        parent_energy = fittingFunctions.energy_new(parent.grid[0])
        child_energy = fittingFunctions.energy_new(child.grid[0])
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
    solution = evolution_spring(first_grid, fps, num_of_mut, "resources/least_square.json")
    viewGrid.printing_dots(solution[0], "first",R)
    viewGrid.printing_dots(solution[-1], "last",R)

