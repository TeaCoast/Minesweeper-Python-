import math
import random

X = 0
Y = 1

CLOSED = 9
FLAG = 10

SYMBOL_MAP = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4', '5': 5, '6': 6, '7': 7, '8': 8,
    CLOSED: '?', FLAG: '%'
}

class MinesweeperAPI:
    grid_size: tuple[int, int]
    cell_count: int
    mine_locations: list[tuple[int, int]]
    mine_count: int

    visual_matrix: list[list[str]]


    def __init__(self, grid_size: tuple[int, int], mine_locations: list[tuple[int, int]] = None, *, mine_count: int = None):
        self.grid_size = grid_size
        self.cell_count = grid_size[X] * grid_size[Y]
        if mine_count is None:
            mine_count = math.sqrt(self.cell_count)
        self.mine_count = mine_count
        if mine_locations is None:
            mine_locations = random.choices(range(self.cell_count), k=self.mine_count)
        self.mine_locations = mine_locations

        self.visual_matrix = [[9] * grid_size[X]] * grid_size[Y]
    
    def count_surrounding_mines(self, cell_location: tuple[int, int]):
        count = 0
        for mine_location in self.mine_locations:
            if (abs(self.mine_locations[X] - cell_location[X]) == 1 and 
                abs(self.mine_locations[Y] - cell_location[Y]) == 1): 
                count += 1
        return count

    def open_cell(self, cell_location: tuple[int, int]):
        if self.visual_matrix[cell_location[Y]][cell_location[X]] == FLAG:
            return None
        if cell_location in self.mine_locations:
            return False
        count = self.count_surrounding_mines(cell_location)
        self.visual_matrix[cell_location[Y]][cell_location[X]] = count

    def flag_cell(self, cell_location: tuple[int, int]):
        if self.visual_matrix[cell_location[Y]][cell_location[X]] <= 8:
            return None
        if self.visual_matrix[cell_location[Y]][cell_location[X]] == CLOSED:
            action = FLAG
        else:
            action = CLOSED
        self.visual_matrix[cell_location[Y]][cell_location[X]] = action

    def __str__(self):
        lines = []
        lines.append('-' * (self.grid_size[0] + 2))
        for line in self.visual_matrix:
            lines.append('|' + '|'.join(SYMBOL_MAP[count] for count in line) + '|')
        lines.append('-' * (self.grid_size[0] + 2))
        return lines

minesweeperAPI = MinesweeperAPI((5, 5))
