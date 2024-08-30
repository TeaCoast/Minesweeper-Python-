import math
import random

point = tuple[int, int]

X = 0
Y = 1

CLOSED = 9
FLAG = 10
MINE = 11

SYMBOL_MAP = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4', '5': 5, '6': 6, '7': 7, '8': 8,
    CLOSED: '?', FLAG: '%', MINE: '#'
}

INVALID = 0
SUCCESS = 1
LOSE = 2
WIN = 3

class MinesweeperAPI:
    grid_size: point
    cell_count: int
    mine_locations: list[point]
    mine_count: int

    visual_matrix: list[list[str]]


    def __init__(self, grid_size: point, 
                 mine_locations: list[point] = None, *, 
                 mine_count: int = None):
        self.grid_size = grid_size
        self.cell_count = grid_size[X] * grid_size[Y]
        if mine_count is None:
            mine_count = math.sqrt(self.cell_count)
        self.mine_count = mine_count
        if mine_locations is None:
            mine_locations = random.choices(range(self.cell_count), k=self.mine_count)
        self.mine_locations = mine_locations

        self.visual_matrix = [[9] * grid_size[X]] * grid_size[Y]

    def get_cell(self, cell_location: point):
        return self.visual_matrix[cell_location[Y]][cell_location[X]]
    def set_cell(self, cell_location: point, value: int):
        self.visual_matrix[cell_location[Y]][cell_location[X]] = value

    def is_in_grid(self, cell_location: point):
        return (0 <= cell_location[X] < self.grid_size[X] and 
                0 <= cell_location[Y] < self.grid_size[Y])

    def count_surrounding_mines(self, cell_location: point):
        count = 0
        for mine_location in self.mine_locations:
            if (abs(self.mine_locations[X] - cell_location[X]) == 1 and 
                abs(self.mine_locations[Y] - cell_location[Y]) == 1): 
                count += 1
        return count

    def open_cell(self, cell_location: point):
        if self.get_cell(cell_location) != CLOSED:
            return INVALID
        if cell_location in self.mine_locations:
            self.set_cell(cell_location, MINE)
            return LOSE
        count = self.count_surrounding_mines(cell_location)
        self.set_cell(cell_location, count)
        return SUCCESS

    def flag_cell(self, cell_location: point):
        if self.get_cell(cell_location) <= 8:
            return INVALID
        if self.get_cell(cell_location) == CLOSED:
            action = FLAG
        else:
            action = CLOSED
        self.set_cell(cell_location, action)
        return SUCCESS

    def __str__(self):
        lines = []
        lines.append('|' + '|'.join(column_i % 10 for column_i in range(self.grid_size[X])) + '|')
        lines.append('|' + "-|" * self.grid_size[X])
        for row_i, line in enumerate(self.visual_matrix):
            lines.append(str(row_i % 10) + '|' + '|'.join(SYMBOL_MAP[count] for count in line) + '|')
        lines.append('-' * (self.grid_size[X] + 2))
        return lines

minesweeperAPI = MinesweeperAPI((5, 5))
game_over = False

OPEN_STATE = False
FLAG_STATE = True

STATE_MAP = {OPEN_STATE: "open mode", FLAG_STATE: "flag mode"}

edit_state = OPEN_STATE

while not game_over:
    position: point = None
    retry = False
    while position is None:
        if retry:
            print("Invalid input, try again")
        user_input = input(f"Enter a position (x y) or enter to switch edit mode ({STATE_MAP[edit_state]}) to {STATE_MAP[not edit_state]}:").strip()
        if user_input == '':
            edit_state = not edit_state
        elif user_input.count(' ') == 1 and user_input.replace(' ', '').isdigit():
            x, y = user_input.split(' ')
            if minesweeperAPI.is_in_grid((x, y)):
                position = (x, y)
        retry = True
    if edit_state == OPEN_STATE:
        result = minesweeperAPI.open_cell(position)
        if result == LOSE:
            game_over = True
            print("you have lost")
        elif result == INVALID:
            print("invalid input, try again")
    elif edit_state == FLAG_STATE:
        result = minesweeperAPI.flag_cell(position)
    print(minesweeperAPI)
    