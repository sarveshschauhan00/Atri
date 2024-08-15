import os
import shutil
from reader import get_directory_structure_as_string
from team import product_manager, project_manager, designer, developer, tester


BASE_FOLDER = "project"

codetype_names = {
    'html': 'html\n',
    'css': 'css\n',
    'js': 'javascript\n',
    'py': 'python\n',
    'vue': 'vue\n',
    'csv': 'csv\n',
    'json': 'json\n',
    'txt': 'plaintext\n'
}


class ProjectCreator:
    def __init__(self, project_info) -> None:
        self.project_details = product_manager(project_info)
        # print(self.project_details)

        self.instructions = project_manager(self.project_details)
        print(self.instructions)

        self.file_structure = ""

        self.file_codes = {}


        


class ProjectAnalyzer:
    def __init__(self) -> None:
        # Generate and print the directory structure for the selected project
        project_path = os.path.join('project')
        directory_structure = get_directory_structure_as_string(project_path)

        self.project_description = ""
        
        self.file_structure = directory_structure
        self.file_paths = {}
        self.file_codes = {}
        self.file_summeries = {}



def content_writer(file_path, content):
    with open(os.path.join(BASE_FOLDER, file_path), 'w') as f:
        f.write(content)


def clean_directory(directory):
    """Remove all contents of the specified directory."""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def create_file_structure(base_dir, file_structure):
    """Create the specified file structure inside the base directory."""
    for file_path in file_structure:
        full_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if file_path[-1] != '/':
            with open(full_path, 'w') as f:
                pass  # Create an empty file



if __name__=="__main__":
    # project_info = input("Enter complete detail of the project: ")
    project_info = "Create a demo e-commerce website and for database use csv files"
    creator = ProjectCreator(project_info)
