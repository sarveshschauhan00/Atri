import os

from reader import get_directory_structure_as_string

# Generate and print the directory structure for the selected project
project_path = os.path.join('project', os.listdir('project')[0])
directory_structure = get_directory_structure_as_string(project_path)
print(directory_structure)