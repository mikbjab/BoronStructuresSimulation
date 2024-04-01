import dataclasses
from typing import List


@dataclasses.dataclass
class Grid:
    grid: List
    data: dict
    l: int
    R: float
    N_blue: int
    def __init__(self,data,grid=None):
        self.grid = grid
        self.data=data
        self.l = data["size"]
        self.R = data["radius"]
        self.N_blue = data["number_blue"]
