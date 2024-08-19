import os
import shutil
from reader import get_directory_structure_as_string
from team import product_manager
from utils import claude_bot, tag_extractor, quick_bot, gpt_bot
from typing import List


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
        self.requirements = ""
        self.project_details = product_manager(project_info)
        self.brief_summery = gpt_bot("Quickly answer the user query", f"Summerise the given project in short paragraph. Only write the paragraph without narration.\n\nProject description:\n{self.project_details}")
        # print(self.project_details)
        print(self.brief_summery)

        prompt = f"""You are given details of a project inside the tag <project-info>, you have to analyze the project and generate a minimal directory structure for this project with very precise detail of every file and folder name.
Ignore the unnecessery files like virtual environment, etc.
No not create empty directories and test files in directories

Your output will be inside the tag <tree>

<project-info>
{self.project_details}
</project-info>"""
        # print(prompt)
        self.files_content = {}
        self.file_structure = claude_bot(prompt)
        self.file_structure = tag_extractor(self.file_structure, "tree")[0]
        print(self.file_structure)
        clean_directory(BASE_FOLDER)
        self.file_codes = {}
        prompt = f'Analyze the given files structure and create a list of full path of all the files from root directory in order they should have been written and generate full flow chart of these files.\n\nYour output will be a json {{"file_paths":[""], "flow_chart":""}}\n\n\nFile Structure:\n{self.file_structure}'
        response = quick_bot(prompt)
        self.file_paths = response['file_paths']
        self.flow = response['flow_chart']

        # print(self.file_paths)
        # print(self.flow)
        clean_directory(BASE_FOLDER)
        create_file_structure(BASE_FOLDER, self.file_paths)

        prompt = """You are given a project description, it's file structure, list of full path of each file and it's flow.

Analyze the working of the project and assume how files might be inter-linked and inter-dependent.
I want to create a file but it shared or dependent on other files before it should be created. I want you to generate list of paths of all files which I should keep in mind before generating that particular file code.
You understand it very well for any project there has to be a starting point, where first file will be written and based on that second file will be written and based on 1st and 2nd file 3 file will be written. I want you to create a json object containing fisrt file path as key and empty list assigned to it, then second file which may or may not be dependent on the first file depending on situation it will be added in the list and hence list of all file paths which can be edited as text, and value of this key will be a list containing referenced files.
Describe in details and generate output

I want an optimized structure hence only add files which are directly linked files in the respect key list for example, to create html, it should refer css, js, varible names used etc, code or any information needed, different type files can be present in the same list, there can be common item in lists
Your output only contain files with text editor editable files hence ignore all files like png, jpg, mp3, mp4, pdf etc
Your output will be json list inside the tag <output> of type {output}

Project Description:
<project_details>
{project_details}
</project_details>

File Structure:
<file_structure>
{file_structure}
</file_structure>

Flow:
<flow>
{flow}
</flow>


""".format(project_details=self.project_details, file_structure=self.file_structure, flow=self.flow, output='{"full_file_path": ["all_files_paths", ...], ...}')
        # print(prompt)
        self.grouped_files = tag_extractor(claude_bot(prompt, temperature=0.7), 'output')[0]
        print(self.grouped_files)

        prompt = """I want to create a full"""

    def content_summerizer(self, content):
        response = claude_bot(f"Analyze the given content to summerize and brief description related to the project. You have to generate blueprint of the given file, identify the variables, names, functions, classes, inputs outputs format and all necessary details and generate a detailed blueprint which can describe the exact functioning and variable names, also mention how to use this file with other project in technincal and logical manner.\nYour output should be inside the tag <blueprint>\n\nProject description: {self.brief_summery}\n\nContent to summerize:\n<summerize>\n{content}\n</summerize>")
        return tag_extractor(response, 'blueprint')[0]

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
    project_info = """
Create a website to teach ancient indian language Pali.
For database use csv files.
"""
    creator = ProjectCreator(project_info)
