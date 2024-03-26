import numpy as np
import random

class Grid:
    def __init__(self,data,grid=None):
        self.grid = grid
        self.data=data
        self.l = data["size"]
        self.R = data["radius"]
        self.N_blue = data["number_blue"]

    def producing_red_blue_grid(self):
        # number in the grid indicates the type of dot in this place
        # 1 means red
        # 0 means out of bounds
        # -1 means blue
        grid = np.ones((2 * self.l, 2 * self.l), dtype=int)
        number_of_dots = 4 * self.l ** 2
        red = []
        blue = []

        # removing dots that are outside of circle of radius R
        for i in range(-self.l, self.l):
            for j in range(-self.l, self.l):
                # we got here sqrt(3) because we want the dots in hexagonal grid
                if i ** 2 + 2 * i * j / np.sqrt(3) + 4 * j ** 2 / 3 > self.R ** 2:
                    grid[i + self.l, j + self.l] = 0
                    number_of_dots -= 1
                else:
                    red.append([i, j])

        # creating blue dots from dots inside the circle
        for i in range(self.N_blue):
            not_created = True
            while not_created:
                x = random.randint(0, 2 * self.l - 1)
                y = random.randint(0, 2 * self.l - 1)
                if grid[x, y] == 1:
                    grid[x, y] = -1
                    red.remove([x - self.l, y - self.l])
                    blue.append([x - self.l, y - self.l])
                    not_created = False
        self.grid=[red, blue]
