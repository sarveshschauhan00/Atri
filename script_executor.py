import subprocess

# Path to the script
script_path = "./script.sh"

# Run the script
result = subprocess.run(["bash", script_path], capture_output=True, text=True)

# Print the output
print(result.stdout)