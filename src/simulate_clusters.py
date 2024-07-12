from src.simulation import evolution, simulate_clusters, weird_simulate_clusters
from src.util import GridFactory, viewGrid, analysis

if __name__=="__main__":
    fps=50000
    num_of_mut=5
    #first_grid=GridFactory.create_random_gridObject(15,"gauss",0.3, 0.4)
    first_grid=GridFactory.create_from_json("test_grid.json")
    #viewGrid.printing_dots(first_grid, "first","15")
    solution = simulate_clusters(first_grid, fps, num_of_mut,
        [4.0017323750914855, -0.003838679072111818, 0.9253622406755336])
    solution1 =evolution(first_grid,fps,num_of_mut)
    viewGrid.printing_dots(solution, "last clusters 10","15")
    viewGrid.printing_dots(solution1, "last table","15")
    print("initial ratio: ", analysis.calculate_ratio(first_grid))
    print("final ratio: ", analysis.calculate_ratio(solution))