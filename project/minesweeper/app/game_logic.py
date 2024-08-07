import random

class MinesweeperGame:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = self.initialize_grid()
        self.place_mines()
        self.calculate_numbers()
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.victory = False

    def initialize_grid(self):
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def place_mines(self):
        mine_positions = set()
        while len(mine_positions) < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) not in mine_positions:
                mine_positions.add((row, col))
                self.grid[row][col] = -1

    def calculate_numbers(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == -1:
                    continue
                self.grid[row][col] = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.grid[r][c] == -1:
                    count += 1
        return count

    def reveal_cell(self, row, col):
        if self.game_over or self.revealed[row][col] or self.flagged[row][col]:
            return
        self.revealed[row][col] = True
        if self.grid[row][col] == -1:
            self.game_over = True
        elif self.grid[row][col] == 0:
            self.reveal_adjacent_cells(row, col)
        self.check_victory()

    def reveal_adjacent_cells(self, row, col):
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if not self.revealed[r][c]:
                    self.reveal_cell(r, c)

    def flag_cell(self, row, col):
        if not self.revealed[row][col]:
            self.flagged[row][col] = not self.flagged[row][col]

    def check_victory(self):
        if all(self.revealed[row][col] or self.grid[row][col] == -1 for row in range(self.rows) for col in range(self.cols)):
            self.victory = True
            self.game_over = True

    def get_game_state(self):
        return {
            'grid': self.grid,
            'revealed': self.revealed,
            'flagged': self.flagged,
            'game_over': self.game_over,
            'victory': self.victory
        }
