import os

from matplotlib import pyplot as plt

from src.util import analysis
from src.deprecated import fittingFunctions
from src.util import GridFactory as GF
from src.util.viewGrid import printing_dots

if __name__ == "__main__":
    fileNames = os.listdir("../../resources/training_big/")
    training_grids = []
    energies = []
    ratios = []
    for fileName in fileNames:
        if "M3" in fileName:
            temp = GF.create_from_json("../resources/training_big/" + fileName)
            training_grids.append(temp)
            energies.append(fittingFunctions.energy_with_table(temp.grid[0]))
            ratios.append(analysis.calculate_ratio(temp))

    for i in range(5):
        printing_dots(training_grids[i], str(i), i)

    _ = plt.hist(energies, bins=50)
    plt.title("energy histogram")
    plt.show()
    _ = plt.hist(ratios, bins=50)
    plt.title("ratio histogram")
    plt.show()
