import numpy as np
from matplotlib import pyplot as plt
import random

# constants
l = 10
R = 0.8 * l
Nc = 190 # because with this parameters total number of dots is 197

# creating hexagonal grid constrained by circle
square_grid = np.empty([(4 * l * l), 2], dtype=float)
for i in range(-l, l):
    for j in range(-l, l):
        square_grid[(i + l) * 2 * l + j + l] = np.array([i, j])
square_grid = np.swapaxes(square_grid, 0, 1)
shear_matrix = np.array([[1, -np.sqrt(3) / 3], [0, 1]])

hexagonal = np.matmul(shear_matrix, square_grid)
hexagonal = np.swapaxes(hexagonal, 0, 1)

bool_map = []
for i in range(len(hexagonal)):
    if hexagonal[i, 0] ** 2 + hexagonal[i, 1] ** 2 <= R ** 2:
        bool_map.append(True)
    else:
        bool_map.append(False)

hexagonal_constrained = hexagonal[bool_map]
number_of_dots=len(hexagonal_constrained)
print(number_of_dots)
hexagonal_constrained = np.swapaxes(hexagonal_constrained, 0, 1)
square_constrained=np.matmul(np.linalg.inv(shear_matrix),hexagonal_constrained)
print(square_constrained)
# generating blue dots
for i in range(number_of_dots-Nc):
    position=random.randint(0,197)


# printing
hexagonal = np.swapaxes(hexagonal, 0, 1)
plt.scatter(hexagonal_constrained[0,], hexagonal_constrained[1,], s=10)
plt.scatter(square_constrained[0,], square_constrained[1,], s=10)

theta = np.linspace(0, 2 * np.pi, 150)
x_circle = R * np.cos(theta)
y_circle = R * np.sin(theta)
plt.plot(x_circle, y_circle, color="grey")

plt.ylim(-l, l)
plt.xlim(-l, l)
ax = plt.gca()
ax.set_aspect(1)
plt.show()

