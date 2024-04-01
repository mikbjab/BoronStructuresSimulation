import json
import random
from typing import List

import src.util.Grid as Grid
import numpy as np
import src.util.viewGrid as view

class GridFactory:

    @staticmethod
    def createChild(parentGrid, new_positions):
        return Grid.Grid(parentGrid.data, new_positions)

    @staticmethod
    def produce_default_red_grid(gridObject):
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

    @staticmethod
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

    @staticmethod
    def add_random_blue_dots(gridObject):
        l = gridObject.l

        # creating blue dots from dots inside the circle
        for i in range(gridObject.N_blue):
            not_created = True
            while not_created:
                x = random.randint(-l, l)
                y = random.randint(-l, l)
                if [x, y] in gridObject.grid[0]:
                    gridObject.grid[0].remove([x, y])
                    gridObject.grid[1].append([x, y])
                    not_created = False

    @staticmethod
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
    @staticmethod
    def create_from_json(filename):
        with open(filename, "r") as file:
            parameters = json.load(file)
            if parameters["radius"] != -1:
                tempGrid = Grid.Grid({"size": parameters["size"], "radius": parameters["radius"],
                                      "number_blue": parameters["number_blue"]})
                GridFactory.produce_default_red_grid(tempGrid)
                GridFactory.remove_outside_dots(tempGrid)
            else:
                tempGrid = Grid.Grid({"size": parameters["size"], "radius": parameters["radius"],
                                      "number_blue": parameters["number_blue"]}, [parameters["dots"], []])

            if parameters["number_blue"] != -1:
                GridFactory.add_random_blue_dots(tempGrid)
            else:
                GridFactory.add_given_blue_dots(tempGrid, parameters["empty"])

            return tempGrid

    @staticmethod
    def create_from_json_list(filename):
        with open(filename, "r") as file:
            parameters_list = json.load(file)
            list_grid = []
            for item in parameters_list:
                if item["radius"] != -1:
                    tempGrid = Grid.Grid({"size": item["size"], "radius": item["radius"],
                                          "number_blue": -1})
                    GridFactory.produce_default_red_grid(tempGrid)
                    GridFactory.remove_outside_dots(tempGrid)
                else:
                    tempGrid = Grid.Grid({"size": item["size"], "radius": item["radius"],
                                          "number_blue": -1}, [item["dots"], []])
                GridFactory.add_given_blue_dots(tempGrid, [])
                list_grid.append(tempGrid)
            return list_grid

    @staticmethod
    def save_grid(gridObject, filename):
        with open(filename, "w") as file:
            result_data = {"size": gridObject.l, "radius": -1, "number_blue": -1, "dots": gridObject.grid[0],
                           "empty": gridObject.grid[1]}
            json.dump(result_data, file)

    @staticmethod
    def create_semiperiodic_grid_positions(cell_grid, centers_positions):
        atoms = set()
        for center in centers_positions:
            for cell in cell_grid:
                atoms.add(tuple([cell[0] + center[0], cell[1] + center[1]]))
        result=[]
        for atom in atoms:
            result.append(list(atom))
        return Grid.Grid({"size": 20, "radius": -1, "number_blue": -1}, [result, []])

    @staticmethod
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


if __name__ == "__main__":
    cell_grid_b36 = [[1, 0], [2, 0], [3, 0],
                     [-1, 0], [-2, 0], [-3, 0],
                     [0, 1], [1, 1], [2, 1],
                     [-1,1], [-2, 1], [-3, 1],
                     [0, 2], [1, 2], [-1, 2], [-2, 2], [-3, 2],
                     [0, 3], [-1, 3], [-2, 3], [-3, 3],
                     [0, -1], [-1, -1], [-2, -1],
                     [1, -1], [2, -1], [3, -1],
                     [0, -2], [-1, -2], [1, -2], [2, -2], [3, -2],
                     [0, -3], [1, -3], [2, -3], [3, -3]
                     ]
    center_positions_b36=[[0,0],[3,3],[6,-3],[-3,6],[-6,3],[-3,-3],[3,-6]]
    grid_b36=GridFactory.create_semiperiodic_grid_positions(cell_grid_b36,center_positions_b36)
    view.printing_dots(grid_b36,"test b36",1)
    cell_grid_beta12=[[0,0],[1,0],[2,0],[0,1],[1,1]]
    vector_a_b12=[3,0]
    vector_b_b12=[-1,2]
    grid_beta12=GridFactory.create_semiperiodic_grid_vectors(cell_grid_beta12,vector_a_b12,vector_b_b12,range(-3,3),range(9))
    view.printing_dots(grid_beta12,"test beta12",1)

    cell_grid_s5 = [[1, 0], [2, 0],
                     [-1, 0], [-2, 0],
                     [0, 1], [1, 1],
                     [-1,1], [-2, 1],
                     [0, 2], [1, 2], [-1, 2], [-2, 2],
                     [0, -1], [-1, -1],
                     [1, -1], [2, -1],
                     [0, -2], [1, -2], [2, -2]
                     ]
    vector_a_s5=[3,0]
    vector_b_s5=[0,3]
    grid_s5 = GridFactory.create_semiperiodic_grid_vectors(cell_grid_s5, vector_a_s5,vector_b_s5,range(-3,3),range(5))
    view.printing_dots(grid_s5, "test s5", 1)

    cell_grid_x3=[[1,0],[2,0],[-1,0],[-2,0],
                  [1,1],[0,1],[-1,1],[-2,1],
                  [2,-1],[1,-1],[0,-1],[-1,-1]]
    vector_a_x3=[5,0]
    vector_b_x3=[-1,2]
    grid_x3 = GridFactory.create_semiperiodic_grid_vectors(cell_grid_x3, vector_a_x3,vector_b_x3,range(-3,3),range(5))
    view.printing_dots(grid_x3, "test x3", 1)
    GridFactory.save_grid(grid_beta12,"../resources/grid_beta12.json")
    GridFactory.save_grid(grid_b36,"../resources/grid_b36.json")
    GridFactory.save_grid(grid_x3,"../resources/grid_x3.json")
    GridFactory.save_grid(grid_s5,"../resources/grid_s5.json")