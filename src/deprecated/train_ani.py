import json
import os
import random

from matplotlib import pyplot as plt

from src.fitParameters.fit_structures import MSE, random_walk_ani
from src.util import analysis
from src.deprecated import fittingFunctions
from src.util import GridFactory as GF
from src.util.viewGrid import printing_dots

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

    for i in range(5):
        printing_dots(training_grids[i],str(i),i)

    _ = plt.hist(energies, bins='auto')
    plt.title("energy histogram")
    plt.show()
    _ = plt.hist(ratios, bins='auto')
    plt.title("ratio histogram")
    plt.show()

    num_of_training_steps = 100


    k2 = random.uniform(0, 0.8)
    k1 = random.uniform(0, 0.8)
    k3 = random.uniform(0, 0.8)
    k4 = random.uniform(0, 0.8)
    k5 = random.uniform(0, 0.8)
    k6 = random.uniform(0, 0.8)
    initial_guess = [k1, k2, k3,k4,k5,k6]
    print(initial_guess, MSE(initial_guess, training_grids))
    initial_guess = random_walk_ani(initial_guess, num_of_training_steps, training_grids)
    print("final: ", initial_guess, MSE(initial_guess, training_grids))

    with open("../../resources/random_walk_parameters_ani.json", "w") as file:
        json.dump({"k1": initial_guess[0], "k2": initial_guess[1], "k3": initial_guess[2],
                   "k4":initial_guess[3], "k5":initial_guess[4],"k6":initial_guess[5]}, file)

