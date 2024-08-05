import os
import shutil

# Define the base directory
base_dir = 'project'

# Define the file structure
file_structure = [
    'todo-list-app/backend/app/__init__.py',
    'todo-list-app/backend/app/models.py',
    'todo-list-app/backend/app/routes.py',
    'todo-list-app/backend/app/config.py',
    'todo-list-app/backend/run.py',
    'todo-list-app/backend/requirements.txt',
    'todo-list-app/backend/migrations/',
    'todo-list-app/backend/venv/',
    'todo-list-app/frontend/public/index.html',
    'todo-list-app/frontend/src/assets/',
    'todo-list-app/frontend/src/components/TaskList.vue',
    'todo-list-app/frontend/src/components/TaskItem.vue',
    'todo-list-app/frontend/src/components/TaskForm.vue',
    'todo-list-app/frontend/src/store/index.js',
    'todo-list-app/frontend/src/views/',
    'todo-list-app/frontend/src/App.vue',
    'todo-list-app/frontend/src/main.js',
    'todo-list-app/frontend/.gitignore',
    'todo-list-app/frontend/babel.config.js',
    'todo-list-app/frontend/package.json',
    'todo-list-app/frontend/README.md'
]

def clean_directory(directory):
    """Remove all contents of the given directory."""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def create_file_structure(base_dir, file_structure):
    """Create the given file structure inside the base directory."""
    for path in file_structure:
        full_path = os.path.join(base_dir, path)
        dir_path = os.path.dirname(full_path)
        
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        if not path.endswith('/'):
            with open(full_path, 'w') as f:
                pass

# Clean the base directory
clean_directory(base_dir)

# Create the file structure
create_file_structure(base_dir, file_structure)

print("Directory cleaned and file structure created successfully.")
