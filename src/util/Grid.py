import dataclasses
from typing import List


@dataclasses.dataclass
class Grid:
    grid: List
    l: int
    R: float
    def __init__(self,data,grid=None):
        self.grid = grid
        self.l = data["size"]
        self.R = data["radius"]
