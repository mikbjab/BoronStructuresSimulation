import random

import numpy as np

from src.util.GridFactory import GridFactory
from src.util.fittingFunctions import optimization_function

import scipy.optimize as optimize

if __name__=="__main__":
    training_grids = []
    # 10 -> number of randomly generated grids
    # for index in range(10):
    #     training_grids.append(GridFactory.create_from_json(f"../resources/training_selected/grid{index}.json"))
    # training_grids.extend(GridFactory.create_from_json_list("../resources/training_selected/gridList.json"))
    # training_grids = np.array(training_grids)

    training_grids.append(GridFactory.create_from_json(f"../resources/structures/grid_b36.json"))
    training_grids.append(GridFactory.create_from_json(f"../resources/structures/grid_beta12.json"))
    training_grids.append(GridFactory.create_from_json(f"../resources/structures/grid_s5.json"))
    training_grids.append(GridFactory.create_from_json(f"../resources/structures/grid_x3.json"))
    print("begin")
    opt_result=optimize.differential_evolution(optimization_function,[(0,2),(0,2),(0,2)],args=(training_grids,1),
                                               disp=True, init="sobol", maxiter=4000, popsize=50,atol=0.,
                                               tol=0.001, polish=False)
    print(opt_result)
