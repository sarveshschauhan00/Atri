import os

def get_directory_structure_as_string(start_path, indent_level=0):
    directory_structure = ""
    indent = ' ' * 4 * indent_level
    directory_structure += f"{indent}{os.path.basename(start_path)}/\n"
    
    # Iterate over items in the directory
    with os.scandir(start_path) as entries:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                # If entry is a directory, recursively call the function
                directory_structure += get_directory_structure_as_string(entry.path, indent_level + 1)
            else:
                # If entry is a file, add the file name to the structure
                directory_structure += f"{indent}|----{entry.name}\n"
    
    return directory_structure


def file_reader(path):
    with open(path, 'r') as f:
        content = f.read()
    return content



def main():
    # Specify the directory you want to start from
    start_path = 'project'
    directory_structure = get_directory_structure_as_string(start_path)
    
    # Print the entire directory structure as a single string
    print(directory_structure)

if __name__ == "__main__":
    main()