import numpy as np
from matplotlib import pyplot as plt
import pyvista as pv
import numpy as np

from src import simulation
from src.util import models
from src.util.Grid import Grid
import src.util.GridFactory as GridFactory

def save_grid(grid,title,filename):
    temp_red = np.array(grid.grid[0])
    matrix = np.array([[1, 1 / np.sqrt(3)], [0, 1]])
    temp_red = np.swapaxes(np.matmul(matrix, np.swapaxes(temp_red, 0, 1)), 0, 1)
    plt.scatter(temp_red[:, 0], temp_red[:, 1], color="red")
    if grid.grid[1]:
        temp_blue = np.array(grid.grid[1])
        temp_blue = np.swapaxes(np.matmul(matrix, np.swapaxes(temp_blue, 0, 1)), 0, 1)
        plt.scatter(temp_blue[:, 0], temp_blue[:, 1], color="blue")

    plt.ylim(-grid.l, grid.l)
    plt.xlim(-grid.l, grid.l)
    plt.xticks([])
    plt.yticks([])
    ax = plt.gca()
    ax.set_aspect(1)
    plt.title(title)
    plt.savefig(filename)

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
    plt.title(title+" #Atoms="+str(len(grid.grid[0])))
    plt.show()

def print_3d_grid(grid:Grid,R=1.,space_R=-0.1,r=0.5,space_r=1.,distance_z=1.6, filename="grid.svg"):
    pv.set_plot_theme("document")
    a=2*R+space_R
    background_atoms = []
    # background grid
    for atom in grid.grid[1]:
        background_atoms.append(pv.Sphere(R,(atom[0]*a+atom[1]*a/2,atom[1]*a*np.sqrt(3)/2,0)))

    for atom in grid.grid[0]:
        background_atoms.append(pv.Sphere(R,(atom[0]*a+atom[1]*a/2,atom[1]*a*np.sqrt(3)/2,0)))

    boron_atoms=[]
    #boron atoms
    a_boron=2*r+space_r
    for atom in grid.grid[0]:
        boron_atoms.append(pv.Sphere(r,(atom[0]*a_boron+atom[1]*a_boron/2,atom[1]*a_boron*np.sqrt(3)/2,distance_z)))
    #edges between boron atoms
    boron_edges=[]
    for atom in grid.grid[0]:
        if [atom[0] - 1, atom[1]] in grid.grid[0]:
            boron_atoms.append(pv.Cylinder((
                (atom[0]-0.5) * a_boron + atom[1] * a_boron / 2, atom[1] * a_boron * np.sqrt(3) / 2, distance_z),
                radius=0.4*r,
                height=a_boron))
        if [atom[0] + 1, atom[1]] in grid.grid[0]:
            boron_atoms.append(pv.Cylinder((
                (atom[0] + 0.5) * a_boron + atom[1] * a_boron / 2, atom[1] * a_boron * np.sqrt(3) / 2, distance_z),
                radius=0.4*r,
                height=a_boron))
        if [atom[0], atom[1] - 1] in grid.grid[0]:
            boron_atoms.append(pv.Cylinder((
                (atom[0]) * a_boron + (atom[1]-0.5) * a_boron / 2, (atom[1]-0.5) * a_boron * np.sqrt(3) / 2, distance_z),
                radius=0.4*r,
                height=a_boron,
                direction=(a_boron / 2,a_boron * np.sqrt(3) / 2,0)))
        if [atom[0], atom[1] + 1] in grid.grid[0]:
            boron_atoms.append(pv.Cylinder((
                (atom[0]) * a_boron + (atom[1] + 0.5) * a_boron / 2, (atom[1] + 0.5) * a_boron * np.sqrt(3) / 2, distance_z),
                radius=0.6*r,
                height=a_boron,
                direction=(a_boron / 2,a_boron * np.sqrt(3) / 2,0)))
        if [atom[0] + 1, atom[1] - 1] in grid.grid[0]:
            boron_atoms.append(pv.Cylinder((
                (atom[0]+0.5) * a_boron + (atom[1] - 0.5) * a_boron / 2, (atom[1] - 0.5) * a_boron * np.sqrt(3) / 2,
                distance_z),
                radius=0.6*r,
                height=a_boron,
                direction=(-a_boron / 2,a_boron * np.sqrt(3) / 2,0)))
        if [atom[0] - 1, atom[1] + 1] in grid.grid[0]:
            boron_atoms.append(pv.Cylinder((
                (atom[0]-0.5) * a_boron + (atom[1] + 0.5) * a_boron / 2, (atom[1] + 0.5) * a_boron * np.sqrt(3) / 2,
                distance_z),
                radius=0.6*r,
                height=a_boron,
                direction=(-a_boron / 2,a_boron * np.sqrt(3) / 2,0)))

    #triangles
    triangles=[]
    for atom in grid.grid[0]:
        if ([atom[0]+1,atom[1]] in grid.grid[0]) and ([atom[0]+1,atom[1]-1] in grid.grid[0]):
            triangles.append(pv.PolyData(np.array([
                [atom[0]*a_boron+atom[1]*a_boron/2,atom[1]*a_boron*np.sqrt(3)/2,distance_z],
                [(atom[0]+1)*a_boron+atom[1]*a_boron/2,atom[1]*a_boron*np.sqrt(3)/2,distance_z],
                [(atom[0] + 1) * a_boron + (atom[1]-1) * a_boron / 2, (atom[1]-1) * a_boron * np.sqrt(3) / 2, distance_z]
            ]),
            faces=[3,0,1,2]))
        if ([atom[0],atom[1]-1] in grid.grid[0]) and ([atom[0]+1,atom[1]-1] in grid.grid[0]):
            triangles.append(pv.PolyData(np.array([
                [atom[0] * a_boron + atom[1] * a_boron / 2, atom[1] * a_boron * np.sqrt(3) / 2, distance_z],
                [atom[0] * a_boron + (atom[1]-1) * a_boron / 2, (atom[1]-1) * a_boron * np.sqrt(3) / 2, distance_z],
                [(atom[0] + 1) * a_boron + (atom[1] - 1) * a_boron / 2, (atom[1] - 1) * a_boron * np.sqrt(3) / 2,
                 distance_z]
            ]),
            faces=[3,0,1,2]))

    pl = pv.Plotter()
    pl.enable_hidden_line_removal()
    for sphere in background_atoms:
        pl.add_mesh(sphere)
    for sphere in boron_atoms:
        pl.add_mesh(sphere,color="red")
    for edge in boron_edges:
        pl.add_mesh(edge,color="red")
    for triangle in triangles:
        pl.add_mesh(triangle,color="red",opacity=0.4)

    pl.camera.position=(0.,0.,90.)
    pl.camera.Roll(-90.)
    pl.show(screenshot=filename)



if __name__=="__main__":
    param=[-4e-7,1.8601,0.1919]
    temp_grid=GridFactory.create_from_json("../../resources/cluster_-++.json")
    save_grid(temp_grid,f"{param}\n"
                        f"E={float('{:.5}'.format(models.model_clusters_basic(temp_grid,param)))} eV",f"C:/Users/miko9/Desktop/cluster_{param}.jpg")
    print("done")