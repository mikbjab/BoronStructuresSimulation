import json
import os
import random

import src.util.GridFactory as GF
from src.fitParameters.fit_structures import MSE, random_walk
from src.util import analysis
from src.deprecated import fittingFunctions
from matplotlib import pyplot as plt

if __name__=="__main__":
    fileNames=os.listdir("../../resources/training_big/")
    training_grids=[]
    energies=[]
    ratios=[]
    for fileName in fileNames:
        if "M5r" in fileName:
            temp=GF.create_from_json("../resources/training_big/"+fileName)
            training_grids.append(temp)
            energies.append(fittingFunctions.energy_with_table(temp.grid[0]))
            ratios.append(analysis.calculate_ratio(temp))

    _ = plt.hist(energies, bins='auto')
    plt.title("energy histogram")
    plt.show()
    _ = plt.hist(ratios, bins='auto')
    plt.title("ratio histogram")
    plt.show()

    num_of_training_steps = 100


    k2 = random.uniform(0.5, 1)
    k1 = random.uniform(0.0001, k2)
    k3 = random.uniform(0.0001, k1)
    initial_guess = [k1, k2, k3]

    #initial_guess = [0.17, 0.53, 0.06]  # [0.13442410124025683, 1.1100909554658314, 0.004773775067342759]
    print(initial_guess, MSE(initial_guess, training_grids))
    initial_guess = random_walk(initial_guess, num_of_training_steps, training_grids, False)
    print("final: ", initial_guess, MSE(initial_guess, training_grids))

    with open("../../resources/random_walk_parameters.json", "w") as file:
        json.dump({"k1": initial_guess[0], "k2": initial_guess[1], "k3": initial_guess[2]}, file)


