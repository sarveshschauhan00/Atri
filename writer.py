import os
import shutil

# Define the base directory
base_dir = 'project'

# Define the file structure
file_structure = [
    'tic_tac_toe/__init__.py',
    'tic_tac_toe/board.py',
    'tic_tac_toe/player.py',
    'tic_tac_toe/game.py',
    'main.py',
    'README.md',
    'requirements.txt',
    'setup.py'
]

def clean_directory(directory):
    """
    Remove all files and folders inside the given directory.
    """
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def create_file_structure(base_dir, file_structure):
    """
    Create the file structure inside the base directory.
    """
    for file_path in file_structure:
        full_path = os.path.join(base_dir, file_path)
        dir_path = os.path.dirname(full_path)
        
        # Create directories if they don't exist
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        # Create empty files
        with open(full_path, 'w') as f:
            pass

if __name__ == "__main__":
    # Clean the base directory
    clean_directory(base_dir)
    
    # Create the file structure
    create_file_structure(base_dir, file_structure)
    
    print(f"Directory '{base_dir}' has been cleaned and the file structure has been created.")
