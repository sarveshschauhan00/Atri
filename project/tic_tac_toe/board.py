
# tic_tac_toe/board.py

class Board:
    def __init__(self):
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]

    def display(self):
        for row in self.grid:
            print('|'.join(row))
            print('-' * 5)

    def update(self, row, col, mark):
        if self.grid[row][col] == ' ':
            self.grid[row][col] = mark
            return True
        return False

    def is_winner(self, mark):
        # Check rows
        for row in self.grid:
            if all(cell == mark for cell in row):
                return True

        # Check columns
        for col in range(3):
            if all(self.grid[row][col] == mark for row in range(3)):
                return True

        # Check diagonals
        if all(self.grid[i][i] == mark for i in range(3)):
            return True
        if all(self.grid[i][2 - i] == mark for i in range(3)):
            return True

        return False

    def is_draw(self):
        return all(cell != ' ' for row in self.grid for cell in row)
