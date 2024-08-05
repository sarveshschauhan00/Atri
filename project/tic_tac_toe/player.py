
# tic_tac_toe/player.py

class Player:
    def __init__(self, mark):
        self.mark = mark

    def get_move(self):
        while True:
            try:
                row = int(input(f"Player {self.mark}, enter the row (0, 1, or 2): "))
                col = int(input(f"Player {self.mark}, enter the column (0, 1, or 2): "))
                if row in [0, 1, 2] and col in [0, 1, 2]:
                    return row, col
                else:
                    print("Invalid input. Please enter numbers between 0 and 2.")
            except ValueError:
                print("Invalid input. Please enter valid integers.")
