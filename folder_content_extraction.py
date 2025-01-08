import os


def get_folder_details(root_path):
    """
    Traverse a folder structure starting from the given root path and collect 
    the content of text files into a single string, while skipping specific files 
    and irrelevant folders (like environment folders, image, and video files).

    Args:
        root_path (str): The root directory path to start the traversal.

    Returns:
        str: A concatenated string containing the paths and content of text files 
             encountered during the traversal, except those explicitly excluded.

    Note:
        Files named "gen_code.txt" and "gen_api_contract.txt" are ignored.
        Common environment folders like 'venv', 'env', '.git', etc. are skipped.
        Image and video files are also skipped.
    """
    text = ""  # Initialize an empty string to store collected content.

    # Define folder names to exclude
    exclude_folders = {
    "myenv","venv", "env", ".git", "__pycache__", ".tox", ".idea", ".vscode", "node_modules", "dist", "build", 
    "target", "out", ".cache", "tmp", ".env", ".pytest_cache", ".coverage", ".gradle", ".m2", "vendor", ".nox", 
    ".tox", ".bundle", "CMakeFiles", ".DS_Store", "Thumbs.db", "*.log", "*.bak", "*.swp", "*.swo", "*.tmp", "*.exe", 
    "*.o", "*.a", "*.so", "*.class", "*.gem", "*.tgz", "*.tar", "*.mp4", "*.mp3", "*.jpg", "*.png", "*.gif", "*.bmp", 
    "*.mkv", "*.avi", "*.mov", "*.mpg"}

    # Define file extensions to skip (image and video files)
    exclude_extensions = {".pdf", ".docx",".xlsx", ".csv", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", 
                          ".svg", ".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".mpeg", ".mpg", ".3gp",
                          ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".opus", ".oga", ".weba", ".amr",
                          ".log"
                          }

    # Traverse the directory structure using os.walk.
    for root, dirs, files in os.walk(root_path):
        # Remove directories that are in the exclude list
        dirs[:] = [d for d in dirs if d not in exclude_folders]

        # Iterate through the files in the current directory.
        for file_name in files:
            file_path = os.path.join(root, file_name)  # Construct the full file path.

            # Skip specific files based on their names.
            if file_name in {"gen_code.txt", "gen_api_contract.txt", "relavant_files.txt", "prompt_answer.txt"}:
                continue  # Skip processing these files.

            # Skip files based on their extensions (image/video files).
            if any(file_name.lower().endswith(ext) for ext in exclude_extensions):
                continue  # Skip image and video files.

            # Add the file path to the text output.
            text += f"\n\n Path: {file_path}\n\n"

            # Attempt to read the file content.
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()  # Read the content of the file.
                    text += content  # Append the content to the text output.
            except Exception as e:
                try:
                    with open(file_path, 'r', encoding='utf-16') as file:
                        content = file.read()
                        text += content  # Append the content to the text output.
                        # print(content)
                except Exception as e:
                    print(f"Error reading file: {e}")
                
                # Print an error message if the file cannot be read.
                print(f"    Error reading {file_path}: {e}")

    return text  # Return the collected text.


text = get_folder_details(r"C:\Users\Asus\Desktop\Code Files\Review_Resume_Scorecard")


# Specify the file name
full_path = "folder_content.txt"  # Ensure you have permissions to write to the root folder

# Combine the base path with the file name to get the full path
# full_path = os.path.join(base_path, file_name)

# Write the string to the file
try:
    with open(full_path, "w", encoding='utf-8') as file:
        file.write(text)
    print(f"Generated API contract successfully written to {full_path}")
except PermissionError:
    print("Permission denied: You need elevated privileges to write to the root folder.")
except Exception as e:
    print(f"An error occurred: {e}")