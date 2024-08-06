from openai import OpenAI
import json
import os
import shutil


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


class project_creator:
    def __init__(self) -> None:    
        project_info = input("Enter complete detail of the project: ")
        self.project_details = gpt_bot(
            "Act as a professional consultant, your job is to understand user need and what user wants to create as in project, and according to your understanding describe the working and of the project and how such project should be create in python without using media files. Just describe in detail all the important parts and conerns in englilsh. Do not write any code",
            project_info
            )
        print(self.project_details)

        file_structure = gpt_bot(
            "You are lazy python developer who create small and very clean structured python projects. Your job it to understand user project and create a full project structure with each and every file name at base level with standard naming conventions of files and folder followed for python projects, do not create testing files. Your output must only contain the file structure",
            self.project_details
            )
        self.file_structure = identifier(file_structure)
        print(self.file_structure)

        self.files_code = {}

        self.project_directory_creator()

        self.file_writer()

    def project_directory_creator(self):
        response = quick_bot(f"generate a python list of all the files relative location of the given file structure, list should be sorted according to how the files expected to be written according to the python developer, name of the base directory also return a string showing interdependents files. Your output will be a json of structure" + ' {"files": [""], "flow": ""}' + f"\n\nfile structure:\n{self.file_structure}.")
        
        self.project_files = response["files"]
        self.flow = response["flow"]

        # self.related_files = quick_bot((
        #     "You are a experienced python developer, you are given a file structure "
        #     "and list of all the files, your job is to generate a list of 1-D lists of file paths based on given instructions, "
        #     "where closely related files paths are clubbed together for code analysis, "
        #     "these files should make sense with each other by having possibility of code sharing. "
        #     "And generate list of different such possible combinations. And inner list should be sorted in order of their relation and outer list should also be sorted on the basis of priority "
        #     ". All Generated lists should have common elements with other lists in order to which they are created "
        #     '\n\nYour output must only contain list of lists of such path in json format given-> {"related_files": [[<list of related files path>]]}'
        #     f"\n\nFile Structure:\n{self.file_structure}\n\n\nAll Paths:\n{self.project_files}\n\nRelations:{self.flow}"
        #     ))['related_files']

        print(self.project_files)
        print('\n===========================================\n')
        # print(self.related_files)
        print('\n===========================================\n')
        print(self.flow)

        # Clean the base directory
        clean_directory(BASE_FOLDER)

        # Create the file structure
        create_file_structure(BASE_FOLDER, self.project_files)

    def file_writer(self):
        system_content = """You are a professional software developer with knowledge of all the file structures and standards followed in every language
        you will write compact codes and follows normal standards in naming convention of variables for easy understanding of project
        You are given full project description, files structure, code of related files with relative position.

        Analyze the file structure and and understand the dependencies of files on each other by analyzing the code of each given file write the code for the requested file

"""

        user_content = """Analyze the based on the project description and code of each file and their dependencies on each other and Write a high quality code by keeping track of related files generate code for the file {file_name}
Highly causious of relative paths and imports

Project description:
{project_description}

Project structure:
{structure}

Project life flow: {flow}

"""
        for i in range(len(self.project_files)):

            file = self.project_files[i]
            if file.split('.')[-1].lower() in ['md', 'gitignore', 'jpg', 'jpeg', 'png'] or file in self.files_code:
                continue

            files_code_str = ""
            for k in self.project_files[ max(0, -5+i) :i]:
                files_code_str += f"CODE for FILE NAME and PATH: {self.files_code[k]}:\n" + "="*50 + "\n\n"

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
            self.files_code[file] = code
            content_writer(file, code)



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


def gpt_bot(system_content, user_content, model="gpt-4o", temperature=0.3, max_tokens=4000):
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


def quick_bot(user_content, model="gpt-4o-mini", temperature=0.0):
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
    creator = project_creator()