import os
import re

# The input multi-line string

# Specify the file path
file_name = "gen_code.txt"

# Read the contents of the file
try:
    with open(file_name, "r") as file:
        file_content = file.read()
    print("File successfully read.")
except FileNotFoundError:
    print(f"Error: The file {file_name} does not exist.")
except PermissionError:
    print(f"Permission denied: Unable to access the file {file_name}.")
except Exception as e:
    print(f"An error occurred: {e}")

# The text from the file is now stored in the variable `file_content`


input_string = file_content

# Regular expression to extract code snippets and their file paths
pattern = r"```(\w+)\n# (.+?)\n(.*?)```"

# Iterate through all matches in the input string
matches = re.finditer(pattern, input_string, re.DOTALL)

# Create files and write content
for match in matches:
    language = match.group(1)
    file_path = match.group(2).strip()
    code_content = match.group(3).strip()

    # print(f"Language: {language}")
    # print(f"File Path: {file_path}")
    # print(f"Code Content: {code_content} \n\n\n")

    # Create the directory structure if it doesn't exist
    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as e:
            print(f"Error creating directory: {dir_name}")
            print(e)

    # Write the content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(code_content)

print("Files and folder structure created successfully.")
