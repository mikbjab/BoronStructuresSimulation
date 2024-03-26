import json
import random
import numpy as np
from scipy.optimize import least_squares
from matplotlib import pyplot as plt

from src.util.fittingFunctions import energy_new, energy_spring_from_param
from src.util.GridFactory import GridFactory


def optimization_function(k_parameters,grids,something):
    num_of_grids=len(grids)
    x = np.arange(num_of_grids)
    difference_array=np.zeros_like(x,dtype=float)
    for i in range(num_of_grids):
        true_value=energy_new(grids[i].grid[0])
        guessed_value=energy_spring_from_param(grids[i].grid[0],k_parameters)
        difference_array[i]=guessed_value-true_value
    return difference_array



if __name__=="__main__":
    training_grids=[]
    # 10 -> number of randomly generated grids
    for index in range(20):
        training_grids.append(GridFactory.create_from_json(f"../resources/training_selected/grid{index}.json"))
    training_grids.extend(GridFactory.create_from_json_list("../resources/training_selected/gridList.json"))
    training_grids=np.array(training_grids)
    k2=random.uniform(0.5,1)
    k1=random.uniform(0.0001,k2)
    k3=random.uniform(0.0001,k1)
    initial_guess=[k1,k2,k3]
    opt_result=least_squares(optimization_function,np.array(initial_guess),method="lm",args=(training_grids,1))
    print(opt_result)
    optimal_param=opt_result.get("x")
    x_cordinate=np.arange(len(training_grids))
    y_true=[]
    y_guessed=[]
    for i in range(len(training_grids)):
        y_true.append(energy_new(training_grids[i].grid[0]))
        y_guessed.append(energy_spring_from_param(training_grids[i].grid[0],optimal_param))

    param_dict={"k1": optimal_param[0],"k2":optimal_param[1],"k3":optimal_param[2]}
    with open("../resources/least_square.json","w") as file:
        json.dump(param_dict,file)


    plt.scatter(x_cordinate,y_true,label="true")
    plt.scatter(x_cordinate,y_guessed,label="guessed")
    plt.legend()
    plt.show()

