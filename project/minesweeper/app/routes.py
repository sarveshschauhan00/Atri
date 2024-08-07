from flask import Blueprint, render_template, request, session, jsonify
from .game_logic import MinesweeperGame

# Create a Blueprint for the app
bp = Blueprint('minesweeper', __name__)

def initialize_game(rows, cols, mines):
    """Initialize a new game instance."""
    game = MinesweeperGame(rows, cols, mines)
    return game.get_game_state()

@bp.route('/')
def index():
    # Initialize a new game and store it in the session
    game = MinesweeperGame(rows=10, cols=10, mines=10)
    session['game'] = game  # Store the entire game object
    return render_template('index.html', game_state=game.get_game_state())

@bp.route('/reveal', methods=['POST'])
def reveal():
    # Get the current game from the session
    game = session.get('game')
    if not game:
        return jsonify({'error': 'Game state not found'}), 400

    # Get the cell coordinates from the request
    data = request.json
    row = data.get('row')
    col = data.get('col')

    # Reveal the cell
    game.reveal_cell(row, col)
    session['game'] = game  # Update the game state in the session

    return jsonify(game.get_game_state())

@bp.route('/flag', methods=['POST'])
def flag():
    # Get the current game from the session
    game = session.get('game')
    if not game:
        return jsonify({'error': 'Game state not found'}), 400

    # Get the cell coordinates from the request
    data = request.json
    row = data.get('row')
    col = data.get('col')

    # Flag the cell
    game.flag_cell(row, col)
    session['game'] = game  # Update the game state in the session

    return jsonify(game.get_game_state())