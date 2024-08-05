import os
import shutil

# Define the base directory
base_dir = 'project'

# Define the file structure to create
file_structure = [
    'todo_list_app/app.py',
    'todo_list_app/tasks.py'
]

def clean_directory(directory):
    """
    Remove all files and directories inside the given directory.
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
    for path in file_structure:
        full_path = os.path.join(base_dir, path)
        dir_name = os.path.dirname(full_path)
        
        # Create directories if they don't exist
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        # Create the empty file
        open(full_path, 'w').close()

def main():
    # Clean the base directory
    clean_directory(base_dir)
    
    # Create the specified file structure
    create_file_structure(base_dir, file_structure)
    
    print(f"Cleaned '{base_dir}' and created the specified file structure.")

if __name__ == "__main__":
    main()
