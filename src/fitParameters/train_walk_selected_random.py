import json
import random

from src.fitParameters.fit_structures import generate_structures, MSE, random_walk
import src.util.GridFactory as GridFactory

if __name__=="__main__":
    num_of_training_steps=100
    training_grids=[]
    #10 -> number of randomly generated grids
    # for indexx in range(10):
    #     training_grids.append(GridFactory.create_from_json(f"../resources/training_selected/grid{indexx}.json"))
    # training_grids.extend(GridFactory.create_from_json_list("../resources/training_selected/gridList.json"))

    training_grids.append(GridFactory.create_from_json(f"../resources/structures/grid_b36.json"))
    training_grids.append(GridFactory.create_from_json(f"../resources/structures/grid_beta12.json"))
    training_grids.append(GridFactory.create_from_json(f"../resources/structures/grid_s5.json"))
    training_grids.append(GridFactory.create_from_json(f"../resources/structures/grid_x3.json"))
    for index in range(30):
        training_grids.append(GridFactory.create_from_json(f"../resources/training_evolved/grid{index}.json"))

    k2=random.uniform(0.5,1)
    k1=random.uniform(0.0001,k2)
    k3=random.uniform(0.0001,k1)
    initial_guess=[k1,k2,k3]

    initial_guess=[0.17,0.53,0.06] #[0.13442410124025683, 1.1100909554658314, 0.004773775067342759]
    print(initial_guess, MSE(initial_guess,training_grids))
    initial_guess=random_walk(initial_guess,num_of_training_steps,training_grids,False)
    print("final: ",initial_guess,MSE(initial_guess,training_grids))

    with open("../resources/random_walk_parameters.json", "w") as file:
        json.dump({"k1":initial_guess[0],"k2":initial_guess[1],"k3":initial_guess[2]},file)
