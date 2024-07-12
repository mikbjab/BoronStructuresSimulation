import random

from src.simulation import evolution
import src.util.GridFactory as GridFactory
from src.util.viewGrid import printing_dots


def generate_structures(n,index,directory="training_big",num_steps=30000,num_mut=3):
    for i in range(n):
        s = int(random.uniform(10, 16))
        #print(index)
        variance=random.uniform(0.3,0.5)
        grid=GridFactory.create_random_gridObject(s,"gauss",random.uniform(0.15,0.35),variance)
        printing_dots(grid,str(i)+"first",1)
        temp_grid=evolution(grid,num_steps,num_mut)
        printing_dots(temp_grid,str(i)+"last",1)
        GridFactory.save_grid(temp_grid, f"../../resources/{directory}/grid{index}-{i}.json")
        print("done ",index,"-",i)

def generate_initial_structures(n,index,directory="training_big"):
    for i in range(n):
        s = int(random.uniform(10, 16))
        #print(index)
        variance=random.uniform(0.3,0.5)
        grid=GridFactory.create_random_gridObject(s,"gauss",random.uniform(0.15,0.35),variance)
        printing_dots(grid,str(i)+"first",1)
        GridFactory.save_grid(grid, f"../../resources/{directory}/grid{index}-{i}.json")
        print("done ",index,"-",i)

def generate_known_structures():
    cell_grid_b36 = [[1, 0], [2, 0], [3, 0],
                     [-1, 0], [-2, 0], [-3, 0],
                     [0, 1], [1, 1], [2, 1],
                     [-1, 1], [-2, 1], [-3, 1],
                     [0, 2], [1, 2], [-1, 2], [-2, 2], [-3, 2],
                     [0, 3], [-1, 3], [-2, 3], [-3, 3],
                     [0, -1], [-1, -1], [-2, -1],
                     [1, -1], [2, -1], [3, -1],
                     [0, -2], [-1, -2], [1, -2], [2, -2], [3, -2],
                     [0, -3], [1, -3], [2, -3], [3, -3]
                     ]
    center_positions_b36 = [[0, 0], [3, 3], [6, -3], [-3, 6], [-6, 3], [-3, -3], [3, -6]]
    grid_b36 = GridFactory.create_semiperiodic_grid_positions(cell_grid_b36, center_positions_b36)
    printing_dots(grid_b36, "test b36", 1)
    cell_grid_beta12 = [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1]]
    vector_a_b12 = [3, 0]
    vector_b_b12 = [-1, 2]
    grid_beta12 = GridFactory.create_semiperiodic_grid_vectors(cell_grid_beta12, vector_a_b12, vector_b_b12,
                                                               range(10), range(10))
    printing_dots(grid_beta12, "test beta12", 1)

    cell_grid_s5 = [[1, 0], [2, 0],
                    [-1, 0], [-2, 0],
                    [0, 1], [1, 1],
                    [-1, 1], [-2, 1],
                    [0, 2], [1, 2], [-1, 2], [-2, 2],
                    [0, -1], [-1, -1],
                    [1, -1], [2, -1],
                    [0, -2], [1, -2], [2, -2]
                    ]
    vector_a_s5 = [3, 0]
    vector_b_s5 = [0, 3]
    grid_s5 = GridFactory.create_semiperiodic_grid_vectors(cell_grid_s5, vector_a_s5, vector_b_s5,
                                                           range(10), range(10))
    printing_dots(grid_s5, "test s5", 1)

    cell_grid_x3 = [[1, 0], [2, 0], [-1, 0], [-2, 0],
                    [1, 1], [0, 1], [-1, 1], [-2, 1],
                    [2, -1], [1, -1], [0, -1], [-1, -1]]
    vector_a_x3 = [5, 0]
    vector_b_x3 = [-1, 2]
    grid_x3 = GridFactory.create_semiperiodic_grid_vectors(cell_grid_x3, vector_a_x3, vector_b_x3,
                                                           range(10), range(10))
    printing_dots(grid_x3, "test x3", 1)
    GridFactory.save_grid(grid_beta12, "../../resources/structures/grid_beta12.json")
    GridFactory.save_grid(grid_b36, "../../resources/structures/grid_b36.json")
    GridFactory.save_grid(grid_x3, "../../resources/structures/grid_x3.json")
    GridFactory.save_grid(grid_s5, "../../resources/structures/grid_s5.json")

if __name__=="__main__":
    generate_structures(700,"M5r-S200k-G-p30",num_steps=200000,num_mut=5)
    #generate_initial_structures(200,"-init")


