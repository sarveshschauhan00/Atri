import os
import shutil

# Define the base directory
base_dir = 'project'

# Define the file structure
file_structure = [
    'minesweeper/__init__.py', 
    'minesweeper/game.py', 
    'minesweeper/board.py', 
    'minesweeper/cell.py', 
    'minesweeper/ui.py', 
    'main.py', 
    'README.md', 
    'requirements.txt', 
    'assets/images/mine.png', 
    'assets/images/flag.png', 
    'assets/images/numbers/0.png', 
    'assets/images/numbers/1.png', 
    'assets/images/numbers/2.png', 
    'assets/images/numbers/3.png', 
    'assets/images/numbers/4.png', 
    'assets/images/numbers/5.png', 
    'assets/images/numbers/6.png', 
    'assets/images/numbers/7.png', 
    'assets/images/numbers/8.png'
]

def clean_directory(directory):
    """
    Remove all contents of the specified directory.
    """
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def create_file_structure(base_dir, file_structure):
    """
    Create the specified file structure inside the base directory.
    """
    for file_path in file_structure:
        full_path = os.path.join(base_dir, file_path)
        dir_name = os.path.dirname(full_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(full_path, 'w') as f:
            pass  # Create an empty file

# Clean the base directory
clean_directory(base_dir)

# Create the specified file structure
create_file_structure(base_dir, file_structure)

print("Directory cleaned and file structure created successfully.")
