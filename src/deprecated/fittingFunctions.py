import json

import numpy as np

from src.util import Grid

# Function of energy of a particle dependent on a number of his neighbors
energy_table = [0., 1.7803, 5.1787, 5.6504, 6.2522, 6.5718, 6.5116]


# calculating energy of given configuration with energy_table
def energy_with_table(red_positions):
    energy = 0.
    for i in range(len(red_positions)):
        neighbours = 0
        if [red_positions[i][0] - 1, red_positions[i][1]] in red_positions:
            neighbours += 1
        if [red_positions[i][0] + 1, red_positions[i][1]] in red_positions:
            neighbours += 1
        if [red_positions[i][0], red_positions[i][1] - 1] in red_positions:
            neighbours += 1
        if [red_positions[i][0], red_positions[i][1] + 1] in red_positions:
            neighbours += 1
        if [red_positions[i][0] + 1, red_positions[i][1] - 1] in red_positions:
            neighbours += 1
        if [red_positions[i][0] - 1, red_positions[i][1] + 1] in red_positions:
            neighbours += 1
        energy += energy_table[neighbours]
    return energy/len(red_positions)

#calculating energy of given configuration using spring model with parameters in json file
def energy_spring_from_file(red_pos, filename):
    count=parameters_count(red_pos)
    with open(filename,"r") as file:
        k_parameters=json.load(file)
        return energy_k(count,k_parameters["k1"],k_parameters["k2"],k_parameters["k3"])

#calculating energy of given configuration using spring model with parameters explictly given
def energy_spring_from_param(red_pos, param):
    count=parameters_count(red_pos)
    return energy_k(count,param[0],param[1],param[2])

#given that the distances d_nn,d_2nn,d_3nn are constant, to calculate the energy we only have to count
# how many times each distance is occurring
def parameters_count(red_points):
    result_count=[0,0,0] #occurrence of [d_nn,d_2nn,d_3nn]
    number_of_points=len(red_points)
    for i in range(number_of_points):
        d_2nn_neighbors=[[red_points[i][0]-1,red_points[i][1]],
                        [red_points[i][0]+1,red_points[i][1]],
                        [red_points[i][0],red_points[i][1]-1],
                        [red_points[i][0],red_points[i][1]+1],
                        [red_points[i][0]+1,red_points[i][1]-1],
                        [red_points[i][0]-1,red_points[i][1]+1]]
        d_nn_neighbors=[[red_points[i][0]-2,red_points[i][1]+1],
                        [red_points[i][0]-1,red_points[i][1]+2],
                        [red_points[i][0]+1,red_points[i][1]+1],
                        [red_points[i][0]+2,red_points[i][1]-1],
                        [red_points[i][0]+1,red_points[i][1]-2],
                        [red_points[i][0]-1,red_points[i][1]-1]]
        d_3nn_neighbors=[[red_points[i][0]-2,red_points[i][1]],
                         [red_points[i][0]+2,red_points[i][1]],
                         [red_points[i][0],red_points[i][1]-2],
                         [red_points[i][0],red_points[i][1]+2],
                         [red_points[i][0]-2,red_points[i][1]+2],
                         [red_points[i][0]+2,red_points[i][1]-2]]
        result_count[0]+=sum(1 for point in d_nn_neighbors if point in red_points)
        result_count[1]+=sum(1 for point in d_2nn_neighbors if point in red_points)
        result_count[2]+=sum(1 for point in d_3nn_neighbors if point in red_points)
    result_count=[item/number_of_points for item in result_count]
    return result_count

def energy_k(count,k1,k2,k3):
    return count[0]*k1*3+count[1]*k2*1+count[2]*k3*4


def optimization_function(k_parameters,grids,something):
    num_of_grids=len(grids)
    mean_square_err=0.
    for i in range(num_of_grids):
        true_value=energy_with_table(grids[i].grid[0])
        guessed_value=energy_spring_from_param(grids[i].grid[0],k_parameters)
        mean_square_err+=np.power(guessed_value-true_value,2)
    return mean_square_err/num_of_grids

def optimization_function_least_square(k_parameters,grids,something):
    num_of_grids=len(grids)
    difference_array=[]
    for i in range(num_of_grids):
        true_value=energy_with_table(grids[i].grid[0])
        guessed_value=energy_spring_from_param(grids[i].grid[0],k_parameters)
        difference_array.append(guessed_value-true_value)
    return np.array(difference_array)/num_of_grids


#neighbours corresponding to matrix elements:
#[(-1,1),(0,1),none]
#[(-1,0),none,(1,0)]
#[none,(0,-1),(1,-1)]
def anisotropic_model(grid,anisotropic_matrix):
    result=[0,0,0,0,0,0]
    for atom in grid.grid[0]:
        if [atom[0]-1,atom[1]+1] in grid.grid[0]:
            result[0]+=1
        if [atom[0],atom[1]+1] in grid.grid[0]:
            result[1]+=1
        if [atom[0]-1,atom[1]] in grid.grid[0]:
            result[2]+=1
        if [atom[0]+1,atom[1]] in grid.grid[0]:
            result[3]+=1
        if [atom[0],atom[1]-1] in grid.grid[0]:
            result[4]+=1
        if [atom[0]+1,atom[1]-1] in grid.grid[0]:
            result[5]+=1
    energy=0
    for i in range(6):
        energy+=result[i]*anisotropic_matrix[i]
    return energy

# model by counting clusters:
# equilateral triangles
# 3 atoms in line
# obtuse triangles
def clusters_model_basic(grid: Grid, coefficients):
    result=[0,0,0]
    for atom in grid.grid[0]:
        if [atom[0] + 1, atom[1]-1] in grid.grid[0]:
            if [atom[0]+1, atom[1]] in grid.grid[0]:
                result[0]+=1
            if [atom[0]+2, atom[1]-1] in grid.grid[0]:
                result[1]+=1
            if [atom[0]+2, atom[1]-2] in grid.grid[0]:
                result[2]+=1
            if [atom[0]+1, atom[1]-2] in grid.grid[0]:
                result[1]+=1
            if [atom[0]-1, atom[1]] in grid.grid[0]:
                result[1]+=1
        if [atom[0], atom[1] - 1] in grid.grid[0]:
            if [atom[0] + 1, atom[1]-1] in grid.grid[0]:
                result[0] += 1
            if [atom[0] + 1, atom[1] - 2] in grid.grid[0]:
                result[1] += 1
            if [atom[0] - 2, atom[1]] in grid.grid[0]:
                result[2] += 1
            if [atom[0] - 1, atom[1] - 1] in grid.grid[0]:
                result[1] += 1
            if [atom[0] + 1, atom[1]] in grid.grid[0]:
                result[1] += 1
        if ([atom[0]-1, atom[1]] in grid.grid[0]) and ([atom[0]+1, atom[1]] in grid.grid[0]):
            result[2]+=1
    energy = 0
    for i in range(3):
        energy += result[i] * coefficients[i]
    return energy/len(grid.grid[0])