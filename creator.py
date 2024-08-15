from openai import OpenAI
import json
import os
import shutil
from reader import get_directory_structure_as_string


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
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
        self.project_details = gpt_bot(
            "Act as a professional consultant, your job is to understand user need and what user wants to create as in project, and according to your understanding describe the features of this project. Give this project a name and working of this project in detail in very clear language in less than 1000 words. Do not write any code",
            project_info
            )
        print(self.project_details)

        file_structure = gpt_bot(
            "You are lazy python developer who create small and very clean structured python projects. Your job it to understand project given by user and create a full project structure with each and every file name with standard naming conventions of files and folder followed for python projects, project should be simple and easy to understand. Your output must only contain the file structure",
            self.project_details
            )
        self.file_structure = identifier(file_structure)
        print(self.file_structure)

        self.file_codes = {}

        self.project_directory_creator()

        print(self.file_paths)
        print(self.flow)
        print(self.packages)

        # self.file_writer()

    def project_directory_creator(self):
        response = quick_bot(
            f"As a professional software developer analyze the given file structure and understand the project and it's functioning and do the following:\n1. generate a python list of string of all files path from root directory and list should be sorted in accordance to the how they should be created"
            "\n2. create flow of the project files in one long string\n\n"
            "Your output will be a json of structure" + ' {"files": [""], "flow": ""}' + f"\n\nfile structure:\n{self.file_structure}."
        )
        self.file_paths = response["files"]
        self.flow = response["flow"]

        output = '{"isolated_groups": [[<files paths>]]}'
        response = quick_bot(
            f'''Act as a professional python developer. You are given project description, it's file structure and file paths
Analyze given project description and it's file structure your job is to analyze dependencies of files on each other.
Then group then similar to packages, where each group has file paths in order in which they should be created in the group
create a list of 1-D list containing isolated groups of files which are isolated and not dependent on other file groups.
Your output will be of structure- {output}

file structure:-
{self.file_structure}

file paths:- {self.file_paths}

Project Description:-
{self.project_details}
            '''
        )
        self.packages = response['isolated_groups']


        # Clean the base directory
        clean_directory(BASE_FOLDER)

        # Create the file structure
        create_file_structure(BASE_FOLDER, self.file_paths)


    def file_writer(self):
        system_content = """You are a professional software developer with knowledge of all the file structures and standards followed in every language
        you will write compact codes and follows normal standards in naming convention of variables for easy understanding of project
        You are given full project description, files structure, code of related files with relative position.

        Analyze the file structure and and understand the dependencies of files on each other by analyzing the code of each given file write the code for the requested file

"""

        user_content = """Analyze the based on the project description and code of each file and their dependencies on each other and Write a high quality code by keeping track of related files generate code for the file {file_name}
Be very careful of relative paths and imports and only do correct imports

Project description:
{project_description}

Project structure:
{structure}

Project life flow: {flow}

"""
        for i in range(len(self.file_paths)):

            file = self.file_paths[i]
            if file.split('.')[-1] in ['md', 'gitignore', 'jpg', 'jpeg', 'png'] or file in self.file_codes:
                continue

            files_code_str = ""
            for k in self.file_paths[ max(0, -5+i) :i]:
                if k.split('.')[-1] in ['md', 'gitignore', 'jpg', 'jpeg', 'png'] or k in self.file_codes:
                    continue
                files_code_str += f"CODE for FILE NAME and PATH: {self.file_codes[k]}:\n" + "="*50 + "\n\n"

            print("Generating code for: ", file)
            # print(files_code_str)

            code = identifier(
                gpt_bot(
                    system_content,
                    user_content.format(
                        file_name=file, 
                        structure=self.file_structure, 
                        project_description=self.project_details, 
                        flow=self.flow) + files_code_str
                    )
                ).replace(codetype_names[file.split('.')[-1]], "")
            self.file_codes[file] = code
            content_writer(file, code)


        


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


def identifier(content):
    i = 0
    for i in range(len(content)):
        if content[i:i+3] == "```":
            i = i+3
            break
    j = 0
    count = 0
    for j in range(len(content)):
        if content[j:j+3] == "```":
            if count == 1:
                break
            else:
                count += 1
    return content[i:j]


def gpt_bot(system_content, user_content, model="gpt-4o", temperature=0.2, max_tokens=4000):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


def quick_bot(user_content, model="gpt-4o-mini", temperature=0.2):
    system_content = """Quickly respond to the user query. Your output will be a json based on user query."""
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        temperature=temperature,
        max_tokens=4096
    )
    # print(response)
    return json.loads(response.choices[0].message.content)


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