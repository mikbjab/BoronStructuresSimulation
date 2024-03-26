import json

# Function of energy of a particle dependent on a number of his neighbors
energy_table = [0., 1.7803, 5.1787, 5.6504, 6.2522, 6.5718, 6.5116]


# calculating energy of given configuration with energy_table
def energy_new(temp_red):
    energy = 0.
    for i in range(len(temp_red)):
        neighbours = 0
        if [temp_red[i][0]-1,temp_red[i][1]] in temp_red:
            neighbours += 1
        if [temp_red[i][0]+1,temp_red[i][1]] in temp_red:
            neighbours += 1
        if [temp_red[i][0],temp_red[i][1]-1] in temp_red:
            neighbours += 1
        if [temp_red[i][0],temp_red[i][1]+1] in temp_red:
            neighbours += 1
        if [temp_red[i][0]+1,temp_red[i][1]-1] in temp_red:
            neighbours += 1
        if [temp_red[i][0]-1,temp_red[i][1]+1] in temp_red:
            neighbours += 1
        energy += energy_table[neighbours]
    return energy/len(temp_red)

#calculating energy of given configuration using spring model with parameters in json file
def energy_spring_from_file(temp_red, filename):
    count=parameters_count(temp_red)
    with open(filename,"r") as file:
        k_parameters=json.load(file)
        return energy_k(count,k_parameters["k1"],k_parameters["k2"],k_parameters["k3"])

#calculating energy of given configuration using spring model with parameters explictly given
def energy_spring_from_param(temp_red, param):
    count=parameters_count(temp_red)
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
    return count[0]*k1*3+count[1]*k2+count[2]*k3*4