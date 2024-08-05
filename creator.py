from openai import OpenAI
import json
import os


client = OpenAI(api_key="sk-proj-h2ACTULQJBaXBC9K16gXT3BlbkFJVAHzm0cl1pUahrAz98Zi")
BASE_FOLDER = "project"


class project_creator:
    def __init__(self) -> None:    
        project_info = input("Enter complete detail of the project: ")
        self.project_details = gpt_bot(
            "Act as a professional consultant, your job is to understand user need and what user wants to create as in project, and according to your understanding describe the working and of the project and how such project should be create in python without using media files. Just describe in english without writing any code",
            project_info
            )
        # print(self.project_details)

        file_structure = gpt_bot(
            "You are lazy python developer who create small and very clean structured python projects without using media files like music or images. Your job it to understand user project and create a full project structure with standard naming conventions of files and folder followed for python projects, do not create testing files. Your output must only contain the file structure",
            self.project_details
            )
        self.file_structure = identifier(file_structure)
        print(self.file_structure)

        self.files_code = {}

        self.project_directory_creator()
        self.file_writer()

    def project_directory_creator(self):
        response = quick_bot(f"generate a python list of all the files relative location of the given file structure, list should be sorted according to how the files expected to be written according to the python developer, name of the base directory also return a string showing extected imports flow of pythons files only on one another. Your output will be a json of structure" + ' {"files": [""], "flow": ""}' + f"\n\nfile structure:\n{self.file_structure}.")
        self.project_files = response["files"]
        self.flow = response["flow"]
        print(self.project_files)
        print(self.flow)

        system_content = "Be a professional python developer, you have a base directory called 'project', you job is to write a python code to clean everything inside this directory and create all the empty files and folders given by user inside this directory"
        python_code = identifier(gpt_bot(
            system_content,
            f"File structure:\n\n{self.project_files}"
        )).replace("python\n", "")
        with open('writer.py', 'w') as f:
            f.write(python_code)
        # print(python_code)

    def file_writer(self):
        system_content = """You are a professional python developer you will write compact codes and follows normal standards in naming convention of variables for easy understanding of project
        You are given full project description, files structure, their dependencies on each other and files location along with their code.
        Analyze the file structure and and understand the dependencies of files on each other and analyze the code of each given file write the code for the requested file
        
        Be extra care on relative imports on dependent files

        Your output will be a python code only for the requested file"""

        user_content = """Analyze the based on the project description and code of each file and Write a python code for the file {file_name}

Project description:
{project_description}

Extra information: {flow}

"""
        files_code_str = ""
        for file in self.project_files:
            print("Generating code for: ", file)
            if file[-3:] == ".py":
                python_code = identifier(gpt_bot(system_content, user_content.format(file_name=file, project_description=self.project_details, flow=self.flow) + files_code_str)).replace("python", "")
                self.files_code[file] = python_code
                files_code_str += f"Code for file name and location {file} is:\n{self.files_code[file]}\n\n\n"                
                
                content_writer(file, python_code)



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



if __name__=="__main__":
    creator = project_creator()