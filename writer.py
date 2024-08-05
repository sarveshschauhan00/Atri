import os
import shutil

# Define the base directory
base_dir = 'project'

# Define the file structure
file_structure = [
    'todo_app/app.py',
    'todo_app/requirements.txt',
    'todo_app/tasks.csv',
    'todo_app/templates/index.html',
    'todo_app/templates/add_task.html',
    'todo_app/templates/edit_task.html',
    'todo_app/static/styles.css'
]

def clean_directory(directory):
    """Remove all contents of the directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

def create_file_structure(base_dir, file_structure):
    """Create the specified file structure inside the base directory."""
    for path in file_structure:
        full_path = os.path.join(base_dir, path)
        dir_name = os.path.dirname(full_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        open(full_path, 'w').close()

def main():
    # Clean the base directory
    clean_directory(base_dir)
    
    # Create the specified file structure
    create_file_structure(base_dir, file_structure)

if __name__ == '__main__':
    main()
