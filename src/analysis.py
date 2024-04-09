from src.util import viewGrid
from src.util.Grid import Grid
from src.util.GridFactory import GridFactory


def count_triangles(grid: Grid):
    count=0
    for atom in grid.grid[0]:
        if ([atom[0]+1,atom[1]] in grid.grid[0]) and ([atom[0]+1,atom[1]-1] in grid.grid[0]):
            count+=1
        if ([atom[0],atom[1]-1] in grid.grid[0]) and ([atom[0]+1,atom[1]-1] in grid.grid[0]):
            count+=1
    return count

def count_edges(grid: Grid):
    edges=0
    red_positions=grid.grid[0]
    for i in range(len(red_positions)):
        neighbours = 0
        if [red_positions[i][0] - 1, red_positions[i][1]] in red_positions:
            neighbours += 1
        if [red_positions[i][0] + 1, red_positions[i][1]] in red_positions:
            neighbours += 1
        if [red_positions[i][0], red_positions[i][1] - 1] in red_positions:
            neighbours += 1
        if [red_positions[i][0], red_positions[i][1] + 1] in red_positions:
            neighbours += 1
        if [red_positions[i][0] + 1, red_positions[i][1] - 1] in red_positions:
            neighbours += 1
        if [red_positions[i][0] - 1, red_positions[i][1] + 1] in red_positions:
            neighbours += 1

        if neighbours!=6 and neighbours!=0:
            edges+=1
    return edges

def calculate_ratio(grid:Grid):
    return count_edges(grid)/count_triangles(grid)

if __name__=="__main__":
    test_grid=GridFactory.create_from_json_list("resources/training_selected/gridList.json")[0]
    viewGrid.printing_dots(test_grid,"test",1)
    print(count_triangles(test_grid))
    print(count_edges(test_grid))
    print(calculate_ratio(test_grid))