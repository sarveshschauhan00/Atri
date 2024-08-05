
# tic_tac_toe/__init__.py

from .board import Board
from .player import Player
from .game import Game

def main():
    # Initialize the game
    board = Board()
    player1 = Player('X')
    player2 = Player('O')
    game = Game(board, player1, player2)
    
    # Start the game loop
    game.play()

if __name__ == "__main__":
    main()
