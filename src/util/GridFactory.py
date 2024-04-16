import json
import math
import random
from tokenize import String

import src.util.Grid as Grid
import numpy as np


def createChild(parentGrid, new_positions):
    return Grid.Grid(parentGrid.data, new_positions)


def produce_working_space(gridObject: Grid.Grid):
    l = gridObject.l
    r = gridObject.R
    blue = []
    for i in range(-l, l):
        for j in range(-l, l):
            if i ** 2 + i * j + j ** 2 < r ** 2:
                blue.append([i, j])
    gridObject.grid = [[], blue]


def produce_uniform_grid(gridObject: Grid.Grid, percent_fill: float):
    number_of_atoms = math.floor(len(gridObject.grid[1]) * percent_fill)
    l = gridObject.l
    for i in range(number_of_atoms):
        created = False
        while not created:
            x = random.randint(-l, l)
            y = random.randint(-l, l)
            if [x, y] in gridObject.grid[1]:
                gridObject.grid[1].remove([x, y])
                gridObject.grid[0].append([x, y])
                created = True


def produce_gaussian_grid(gridObject: Grid.Grid, percent_fill: float, variance: float):
    number_of_atoms = math.floor(len(gridObject.grid[1]) * percent_fill)
    l = gridObject.l
    for i in range(number_of_atoms):
        created = False
        while not created:
            x = int(random.gauss(0, variance * l))
            y = int(random.gauss(0, variance * l))
            if [x, y] in gridObject.grid[1]:
                gridObject.grid[1].remove([x, y])
                gridObject.grid[0].append([x, y])
                created = True


def produce_default_red_grid(gridObject: Grid.Grid):
    l = gridObject.l
    R = gridObject.R
    # number in the grid indicates the type of dot in this place
    # 1 means red
    # 0 means out of bounds
    # -1 means blue
    empty_grid = np.ones((2 * l, 2 * l), dtype=int)
    number_of_dots = 4 * l ** 2
    red = []
    for i in range(-l, l):
        for j in range(-l, l):
            red.append([i, j])

    gridObject.grid = [red, []]


def remove_outside_dots(gridObject):
    l = gridObject.l
    R = gridObject.R
    # removing dots that are outside of circle of radius R
    for i in range(-l, l):
        for j in range(-l, l):
            # we got here sqrt(3) because we want the dots in hexagonal grid
            if i ** 2 + 2 * i * j / np.sqrt(3) + 4 * j ** 2 / 3 > R ** 2:
                gridObject.grid[0].remove([i, j])
                gridObject.grid[1].append([i, j])


def add_random_blue_dots(gridObject, percent: float = 0.15):
    l = gridObject.l

    # creating blue dots from dots inside the circle
    for i in range(int(percent * len(gridObject.grid[0]))):
        not_created = True
        while not_created:
            x = random.randint(-l, l)
            y = random.randint(-l, l)
            if [x, y] in gridObject.grid[0]:
                gridObject.grid[0].remove([x, y])
                gridObject.grid[1].append([x, y])
                not_created = False


def add_given_blue_dots(gridObject, blue_dots):
    for item in blue_dots:
        if item in gridObject.grid[0]:
            gridObject.grid[0].remove(item)
        gridObject.grid[1].append(item)


# structure of json file for creating grid
# size -> creates square grid [-size,size)X[-size,size)
# radius -> radius of circle which simulates plate on which particles are placed,
#   if radius == -1 then you can create custom grid (parameter "dots" needed)
# number_blue -> number of empty places (blue dots on diagrams)
#   if number_blue == -1 then you can specify exactly where empty places are (parameter "empty" needed)
# dots -> exact locations where to place dots (used when radius == -1)
# empty -> exact locations where to change dots to empty (used when number_blue == -1)

def create_from_json(filename):
    with open(filename, "r") as file:
        parameters = json.load(file)
        if parameters["radius"] != -1:
            tempGrid = Grid.Grid({"size": parameters["size"], "radius": parameters["radius"]})
            produce_default_red_grid(tempGrid)
            remove_outside_dots(tempGrid)
        else:
            tempGrid = Grid.Grid({"size": parameters["size"], "radius": parameters["radius"]}, [parameters["dots"], []])

        if "empty" in parameters:
            add_given_blue_dots(tempGrid, parameters["empty"])
        else:
            add_random_blue_dots(tempGrid)

        return tempGrid


def create_from_json_list(filename):
    with open(filename, "r") as file:
        parameters_list = json.load(file)
        list_grid = []
        for item in parameters_list:
            if item["radius"] != -1:
                tempGrid = Grid.Grid({"size": item["size"], "radius": item["radius"]})
                produce_default_red_grid(tempGrid)
                remove_outside_dots(tempGrid)
            else:
                tempGrid = Grid.Grid({"size": item["size"], "radius": item["radius"]}, [item["dots"], []])
            add_given_blue_dots(tempGrid, [])
            list_grid.append(tempGrid)
        return list_grid


def save_grid(gridObject, filename):
    with open(filename, "w") as file:
        result_data = {"size": gridObject.l, "radius": -1, "number_blue": -1, "dots": gridObject.grid[0],
                       "empty": gridObject.grid[1]}
        json.dump(result_data, file)


def create_semiperiodic_grid_positions(cell_grid, centers_positions):
    atoms = set()
    for center in centers_positions:
        for cell in cell_grid:
            atoms.add(tuple([cell[0] + center[0], cell[1] + center[1]]))
    result = []
    for atom in atoms:
        result.append(list(atom))
    return Grid.Grid({"size": 20, "radius": -1, "number_blue": -1}, [result, []])


def create_semiperiodic_grid_vectors(cell_grid, a, b, range_a, range_b):
    atoms = set()
    for i in range_a:
        for j in range_b:
            for cell in cell_grid:
                atoms.add(tuple([cell[0] + a[0] * i + b[0] * j, cell[1] + + a[1] * i + b[1] * j]))
    result = []
    for atom in atoms:
        result.append(list(atom))
    return Grid.Grid({"size": 20, "radius": -1, "number_blue": -1}, [result, []])


def create_random_gridObject(l: int, model: String, percent_fill: float, var: float = None):
    tempGrid = Grid.Grid({"size": l, "radius": 0.8 * l})
    produce_working_space(tempGrid)
    if model == "uniform":
        produce_uniform_grid(tempGrid, percent_fill)
    elif model == "gauss":
        variance = 1 if var is None else var
        produce_gaussian_grid(tempGrid, percent_fill, variance)
    return tempGrid
