
# tic_tac_toe/game.py

class Game:
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1

    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def play(self):
        while True:
            self.board.display()
            row, col = self.current_player.get_move()
            
            if self.board.update(row, col, self.current_player.mark):
                if self.board.is_winner(self.current_player.mark):
                    self.board.display()
                    print(f"Player {self.current_player.mark} wins!")
                    break
                elif self.board.is_draw():
                    self.board.display()
                    print("It's a draw!")
                    break
                else:
                    self.switch_player()
            else:
                print("This cell is already taken. Try again.")
