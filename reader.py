import os
import argparse

# List of files and directories to ignore
IGNORE_LIST = {'.venv', '__pycache__'}
IGNORE_EXTENSIONS = {'.pyc', '.log', '.tmp'}

def get_directory_structure_as_string(start_path):
    """
    Generates a string representing the directory structure with symbols.
    
    Args:
        start_path (str): The root directory path.
        
    Returns:
        str: A string representation of the directory structure.
    """
    lines = []

    def inner(current_path, prefix="", is_last=True):
        basename = os.path.basename(current_path)
        connector = "`-- " if is_last else "|-- "
        lines.append(f"{prefix}{connector}{basename}/" if os.path.isdir(current_path) else f"{prefix}{connector}{basename}")

        if os.path.isdir(current_path):
            # Prepare the prefix for child items
            if is_last:
                new_prefix = prefix + "    "
            else:
                new_prefix = prefix + "|   "

            # Get a sorted list of entries, directories first
            try:
                entries = sorted(os.scandir(current_path), key=lambda e: (not e.is_dir(), e.name.lower()))
            except PermissionError:
                lines.append(f"{new_prefix}Permission Denied")
                return

            # Filter out ignored files and directories
            entries = [
                entry for entry in entries
                if entry.name not in IGNORE_LIST
                and not entry.name.startswith('.')
                and not any(entry.name.endswith(ext) for ext in IGNORE_EXTENSIONS)
            ]

            total = len(entries)
            for idx, entry in enumerate(entries):
                last = (idx == total - 1)
                inner(entry.path, new_prefix, last)

    # Start the recursion with the root directory
    inner(start_path)
    return "\n".join(lines)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Print the directory structure of a specified path.")
    parser.add_argument("--path", type=str, required=True, help="The path to the directory.")
    args = parser.parse_args()

    # Get the directory path from arguments
    start_path = args.path

    # Validate if the path exists
    if not os.path.exists(start_path):
        print(f"Error: The path '{start_path}' does not exist.")
        return

    # Get and print the directory structure
    directory_structure = get_directory_structure_as_string(start_path)
    print(directory_structure)

if __name__ == "__main__":
    main()