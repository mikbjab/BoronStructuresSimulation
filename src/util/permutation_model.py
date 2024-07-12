import copy
import random

from src.util import GridFactory, viewGrid
from src.util.Grid import Grid

class PermutationModel:
    def __init__(self, grid, parameters, oldModel = None):
        if oldModel is None:
            self.empty = grid.grid[1]
            self.atoms = {}
            self.parameters = parameters
            self.energy = 0.
            self.data={"size": grid.l, "radius": grid.R}

            for atom in grid.grid[0]:
                self.add_atom(atom)
                self.energy += self.calculate_atom_energy((atom[0],atom[1]))
        else:
            self.empty=copy.deepcopy(oldModel.empty)
            self.atoms=copy.deepcopy(oldModel.atoms)
            self.parameters=copy.deepcopy(oldModel.parameters)
            self.energy=copy.deepcopy(oldModel.energy)

    def add_atom(self, atom):
        permutation = [1, 2, 3, 4, 5, 6]
        atom_permutation = [0, 0, 0, 0, 0, 0]

        if (atom[0] - 1, atom[1]) in self.atoms:
            permutation.remove(self.atoms.get((atom[0] - 1, atom[1]))[3])
            atom_permutation[0] = self.atoms.get((atom[0] - 1, atom[1]))[3]
        if (atom[0] - 1, atom[1] + 1) in self.atoms:
            permutation.remove(self.atoms.get((atom[0] - 1, atom[1] + 1))[4])
            atom_permutation[1] = self.atoms.get((atom[0] - 1, atom[1] + 1))[4]
        if (atom[0], atom[1] + 1) in self.atoms:
            permutation.remove(self.atoms.get((atom[0], atom[1] + 1))[5])
            atom_permutation[2] = self.atoms.get((atom[0], atom[1] + 1))[5]
        if (atom[0] + 1, atom[1]) in self.atoms:
            permutation.remove(self.atoms.get((atom[0] + 1, atom[1]))[0])
            atom_permutation[3] = self.atoms.get((atom[0] + 1, atom[1]))[0]
        if (atom[0] + 1, atom[1] - 1) in self.atoms:
            permutation.remove(self.atoms.get((atom[0] + 1, atom[1] - 1))[1])
            atom_permutation[4] = self.atoms.get((atom[0] + 1, atom[1] - 1))[1]
        if (atom[0], atom[1] - 1) in self.atoms:
            permutation.remove(self.atoms.get((atom[0], atom[1] - 1))[2])
            atom_permutation[5] = self.atoms.get((atom[0], atom[1] - 1))[2]

        random.shuffle(permutation)

        counter=0
        for i in range(6):
            if atom_permutation[i]==0:
                atom_permutation[i]=permutation[counter]
                counter+=1
        self.atoms[(atom[0], atom[1])] = atom_permutation

    def calculate_atom_energy(self,atom):
        atom_energy=0.
        if (atom[0] - 1, atom[1]) in self.atoms:
            atom_energy+=self.parameters[self.atoms.get(atom)[0]-1]
        if (atom[0] - 1, atom[1] + 1) in self.atoms:
            atom_energy+=self.parameters[self.atoms.get(atom)[1]-1]
        if (atom[0], atom[1] + 1) in self.atoms:
            atom_energy+=self.parameters[self.atoms.get(atom)[2]-1]
        if (atom[0] + 1, atom[1]) in self.atoms:
            atom_energy+=self.parameters[self.atoms.get(atom)[3]-1]
        if (atom[0] + 1, atom[1] - 1) in self.atoms:
            atom_energy+=self.parameters[self.atoms.get(atom)[4]-1]
        if (atom[0], atom[1] - 1) in self.atoms:
            atom_energy+=self.parameters[self.atoms.get(atom)[5]-1]
        return atom_energy

    def count_neighbors(self, atom):
        neighbors=0
        if (atom[0] - 1, atom[1]) in self.atoms:
            neighbors+=1
        if (atom[0] - 1, atom[1] + 1) in self.atoms:
            neighbors+=1
        if (atom[0], atom[1] + 1) in self.atoms:
            neighbors+=1
        if (atom[0] + 1, atom[1]) in self.atoms:
            neighbors+=1
        if (atom[0] + 1, atom[1] - 1) in self.atoms:
            neighbors+=1
        if (atom[0], atom[1] - 1) in self.atoms:
            neighbors+=1
        return neighbors

    def mutate(self, num_atoms):
        random.seed()
        atoms_to_mutate=random.sample(self.atoms.keys(), num_atoms)
        new_positions=random.sample(self.empty, num_atoms)
        for atom in atoms_to_mutate:
            self.energy-=self.calculate_atom_energy(atom)
            self.atoms.pop(atom)
            self.add_atom(new_positions[atoms_to_mutate.index(atom)])
            self.energy+=self.calculate_atom_energy(new_positions[atoms_to_mutate.index(atom)])

    def get_grid(self):
        atom_positions=self.atoms.keys()
        grid0=map(lambda x: [x[0],x[1]],atom_positions)
        return Grid(self.data,[grid0,self.empty])


def simulate(grid:Grid, parameters, steps, mutations):
    init_model=PermutationModel(grid, parameters)
    for i in range(steps):
        new_model=PermutationModel(None, None, init_model)
        new_model.mutate(mutations)
        if new_model.energy > init_model.energy:
            init_model=new_model
            print(i, "  ", init_model.energy)
    return init_model.get_grid()



if __name__ == '__main__':
    num_steps=100000

    first_grid = GridFactory.create_from_json("../test_grid.json")

    viewGrid.printing_dots(first_grid,"initial",1)

    last_grid=simulate(first_grid,[-1,1,1,1,1,1],100000,5)
    viewGrid.printing_dots(last_grid,"final",1)









