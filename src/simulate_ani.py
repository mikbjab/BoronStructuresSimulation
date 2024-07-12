from src.simulation import evolution, simulate_anisotropic
from src.util import GridFactory, viewGrid, analysis

if __name__=="__main__":
    fps=50000
    num_of_mut=5
    first_grid=GridFactory.create_from_json("test_grid.json")
    #viewGrid.printing_dots(first_grid, "first","15")
    solution = simulate_anisotropic(first_grid, fps, num_of_mut,
                                    [0.002481177371343972, 0.01493850033718091, 0.010729827610951542,
                                     0.01587727144024196, 0.016435744282053643, 0.01964248543709471])
    #[0.213803468494253, 0.5826535997946278, 0.09733891086066418] 0.2 MSE
    #[0.009738352045112635, 1.3621416202976369, 0.00024772030574858465] 0.053029140859907384
    solution1 =evolution(first_grid,fps,num_of_mut)
    viewGrid.printing_dots(solution, "last ani 13","15")
    viewGrid.printing_dots(solution1, "last table","15")
    print("initial ratio: ", analysis.calculate_ratio(first_grid))
    print("final ratio: ", analysis.calculate_ratio(solution))