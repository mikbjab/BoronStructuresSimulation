import os
import random


from src.simulation import evolution
from src.util import analysis, GridFactory, viewGrid
from src.util import models
import numpy as np

def simulate_spring():
    params = [[-0.2575234201367123, 2.046648324829256, -0.01679292882896216],
              [-0.2889344628259103, 2.060488666312586, 0.003193992703738759],
              [-0.29181902194097853, 2.06743963249424, 0.0032320152904872397],
              [0.5582733370151663, -9.51082913134378e-06, 0.018024208208159365],
              [0.3460195882857294, -1.7134425082614497e-07, 0.1863475664034404],
              [0.4612953487070791, 1.7971275431197276, -0.4981600320966385],
              [0.041948361159554456, 1.9135759859886727, -0.20628933280026338],
              [0.09906860037619014, 1.1945607113801147, -0.0069422234111360965],
              [0.10322450469197104, 1.2247738326812039, -0.020274939526642763],
              [0.0022349575800987963, 1.225163633969332, 0.058378419196330814],
              [0.03684251528937645, 1.1863638441050544, 0.04450832481303143],
              [-0.17796487674045877, 1.3113308260516026, 0.17110718778168987],
              [-0.1830942377211695, 1.3131389053837446, 0.17437504847158716],
              [0.5335422272716281, -6.797285635887423e-05, 0.04091300505179418],
              [0.540680625307569, -1.1572371556793823e-07, 0.03579596764198417],
              [0.07937021526392884, 1.22253218084183, -0.000609520728759416],
              [0.07514258379004982, 1.2307601153100873, -3.319717634128489e-05]]
    for param in params:
        first_grid = GridFactory.create_from_json("src/test_grid.json")
        solution = evolution(first_grid, 200000, 5
                             , model=models.model_anisotropic
                             , param=param
                             , energy_condition=False)
        viewGrid.save_grid(solution, "spring 150k 5\n" + str(param) + "\n"
                           + "Energy: " + str(models.model_spring(solution, param))
                           , f"spring{params.index(param)}.jpg")

if __name__=="__main__":
    max_value=3
    size=2*max_value+1
    x=np.linspace(-max_value,max_value,size,True)
    y=np.linspace(-max_value,max_value,size,True)
    z=np.linspace(-max_value,max_value,size,True)
    param_x, param_y,param_z=np.meshgrid(x,y,z,indexing="ij")
    for i in (range(size)):
        for j in (range(size)):
            for k in (range(size)):
                param=[param_x[i,j,k],param_y[i,j,k],param_z[i,j,k]]

                if os.path.exists(f"resources/abstract_params/spring/json/spring_{param_x[i,j,k]},{param_y[i,j,k]},{param_z[i,j,k]}.json"):
                   continue
                print(param)
                first_grid = GridFactory.create_from_json("src/test_grid.json")
                solution=evolution(first_grid, 200000, 5
                             , model=models.model_spring
                             , param=param
                             , energy_condition=False)
                GridFactory.save_grid(solution,f"resources/abstract_params/spring/json/spring_{param_x[i,j,k]},{param_y[i,j,k]},{param_z[i,j,k]}.json")
                viewGrid.save_grid(solution,f"spring test 200k 5 steps\n"
                                            f"{param_x[i,j,k]}, {param_y[i,j,k]}, {param_z[i,j,k]}",
                                   f"resources/abstract_params/spring/jpg/spring_{param_x[i,j,k]},{param_y[i,j,k]},{param_z[i,j,k]}.jpg")





