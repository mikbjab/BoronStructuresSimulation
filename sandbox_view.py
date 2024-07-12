from src.simulation import evolution
from src.util import GridFactory, viewGrid, models

# first_grid = GridFactory.create_from_json("resources/abstract_params/spring/json/spring_1.0,-3.0,3.0.json")
#
# viewGrid.print_3d_grid(first_grid,filename="spring1-20.svg")

# first_grid = GridFactory.create_from_json("resources/abstract_params/spring/json/spring_-1.0,2.0,0.0.json")
# viewGrid.printing_dots(first_grid,"1",1)
# viewGrid.print_3d_grid(first_grid,filename="spring-120.svg")
# first_grid = GridFactory.create_from_json("resources/abstract_params/spring/json/spring_-1.0,2.0,1.0.json")
#
# viewGrid.print_3d_grid(first_grid,filename="spring-121.svg")
# first_grid = GridFactory.create_from_json("resources/abstract_params/spring_honey/json/spring_-0.7,2.4,1.3000000000000003.json")
#
# viewGrid.print_3d_grid(first_grid,filename="spring-0.72.41.3.png")
first_grid=GridFactory.create_from_json("src/test_grid.json")
solution=evolution(first_grid, 300000, 5
                             , model=models.model_clusters_basic
                             , param=[-3.0,1.0,1.0]
                             , energy_condition=False)

viewGrid.save_grid(solution,f"cluster model 300k steps\n"
                                            f"[-3.0, 1.0, 1.0]",
                                   f"resources/cluster_comp.jpg")
