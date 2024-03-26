import json

import fit_structures
import src.util.GridFactory as GF

if __name__ == "__main__":
    num_of_test_structures=10
    test_grids=[]
    with open("../resources/fit_parameters1.json", "r") as file:
        data=json.load(file)
        parameters=[data["k1"],data["k2"],data["k3"]]
    for indexx in range(num_of_test_structures):
        test_grids.append(GF.GridFactory.create_from_json(f"../resources/training_selected/grid{indexx}.json"))
    test_grids.extend(GF.GridFactory.create_from_json_list("../resources/training_selected/gridList.json"))

    print(parameters,fit_structures.MSE(parameters,test_grids))