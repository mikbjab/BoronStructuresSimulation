import numpy as np
from matplotlib import pyplot as plt

from src.util import parametersHandling
from src.util.Grid import Grid


def printing_for_animation(grid, ax,R,l):
    temp_red = np.array(grid[0])
    temp_blue = np.array(grid[1])
    matrix = np.array([[1, 1 / np.sqrt(3)], [0, 1]])
    temp_red = np.swapaxes(np.matmul(matrix, np.swapaxes(temp_red, 0, 1)), 0, 1)
    temp_blue = np.swapaxes(np.matmul(matrix, np.swapaxes(temp_blue, 0, 1)), 0, 1)
    ax.clear()
    ax.scatter(temp_red[:, 0], temp_red[:, 1], color="red")
    ax.scatter(temp_blue[:, 0], temp_blue[:, 1], color="blue")
    theta = np.linspace(0, 2 * np.pi, 150)
    x_circle = R * np.cos(theta)
    y_circle = R * np.sin(theta)
    ax.plot(x_circle, y_circle, color="grey")
    ax.set_ylim(-l, l)
    ax.set_xlim(-l, l)

def printing_dots(grid,title,fps):
    temp_red = np.array(grid.grid[0])
    matrix = np.array([[1, 1 / np.sqrt(3)], [0, 1]])
    temp_red = np.swapaxes(np.matmul(matrix, np.swapaxes(temp_red, 0, 1)), 0, 1)
    plt.scatter(temp_red[:, 0], temp_red[:, 1], color="red")
    if grid.grid[1]:
        temp_blue = np.array(grid.grid[1])
        temp_blue = np.swapaxes(np.matmul(matrix, np.swapaxes(temp_blue, 0, 1)), 0, 1)
        plt.scatter(temp_blue[:, 0], temp_blue[:, 1], color="blue")

    theta = np.linspace(0, 2 * np.pi, 150)
    x_circle = grid.R * np.cos(theta)
    y_circle = grid.R * np.sin(theta)
    plt.plot(x_circle, y_circle, color="grey")
    plt.ylim(-grid.l, grid.l)
    plt.xlim(-grid.l, grid.l)
    ax = plt.gca()
    ax.set_aspect(1)
    plt.title(title+" N="+str(fps)+" L="+str(grid.l)+" #Red="+str(len(grid.grid[0])))
    plt.show()

