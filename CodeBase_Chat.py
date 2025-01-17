import os
from dotenv import load_dotenv
import openai
import logging

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


def get_conversation_openai(template, model="gpt-4o-mini", temperature=0.01, max_tokens=None, presence_penalty=0.0, frequency_penalty=0.0):
    """
    Interacts with the OpenAI model based on a provided template.
    
    Args:
        template (str): A string template for generating prompts dynamically.
        model (str, optional): The name of the OpenAI model to use. Defaults to "gpt-4o-mini".
        temperature (float, optional): Sampling temperature. Defaults to 0.1.
        max_tokens (int, optional): Maximum tokens for the response. Defaults to None.
        presence_penalty (float, optional): Presence penalty parameter for the model. Defaults to 0.0.
        frequency_penalty (float, optional): Frequency penalty parameter for the model. Defaults to 0.0.

    Returns:
        str: The content of the response generated by the OpenAI model.
    """

    try:
        # Call the OpenAI Chat API to generate a response
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": template}],
            temperature=temperature,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty
        )

        # Log the API response
        # logging.info("API response: %s", response)

        # Extract and return the content of the response
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error("Error during API call: %s", e)
        return "Error generating response"

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
    "myenv","venv", "env", ".git", "__pycache__", ".tox", ".idea", ".vscode", 
    "node_modules", "dist", "build", "target", "out", ".cache", "tmp", 
    ".env", ".pytest_cache", ".coverage", ".gradle", ".m2", "vendor", 
    ".nox", ".tox", ".bundle", "CMakeFiles", ".DS_Store", "Thumbs.db", 
    "*.log", "*.bak", "*.swp", "*.swo", "*.tmp", "*.exe", "*.o", "*.a", 
    "*.so", "*.class", "*.gem", "*.tgz", "*.tar", "*.mp4", "*.mp3", 
    "*.jpg", "*.png", "*.gif", "*.bmp", "*.mkv", "*.avi", "*.mov", "*.mpg"
    }

    # Define file extensions to skip (image and video files)
    exclude_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg",
                          ".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".mpeg", ".mpg", ".3gp"}

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
                # Print an error message if the file cannot be read.
                print(f"    Error reading {file_path}: {e}")

    return text  # Return the collected text.

# Example usage
folder_path = r"C:\Users\Asus\Desktop\Code Files\Demo_Code_Generator\Django_BackEnd"
folder_path = input("Enter the path of the folder: ")

code_base_context = get_folder_details(folder_path)

user_query = None
# print(test)
while True:
    user_query = input("Please Enter the detailed Question you want to ask on the Code Base: ")
    if user_query.lower() == 'exit':
        break
    else:
        # You can add more code to process the query here if needed
        print(f"You asked: {user_query}")



    # relavent_files_template = f"""
    #     Remember do not change the code of the file. Your task is not to edit the code but to identify the files and 
    #     folders in the given context directory structure which are most relevant to the user query.
    #     You are a folder/files identifier who Identify the files and folders in the given context directory structure 
    #     which are most relanavt to the user query given below:

    #     {user_query}

    #     Give the  complete code of the file with there path which is relevant to the prompt from the context provided.

    #     the context for the  prompt is as follows:

    #     {code_base_context}

    #     Remember to add path before the  code snnipet. 
    #     For example:
    #         ```python
    #         # project_root/app/schemas/user.py

    #         from pydantic import BaseModel

    #         class UserLogin(BaseModel):
    #             username: str
    #             password: str

    #         class UserResponse(BaseModel):
    #             access_token: str
    #             token_type: str
    #         ```
    #     Remember do not change the code of the file. Also remember your task is not to answerr the user query but to 
    #     identify the files and folders in the given context directory structure which are most relevant to the user 
    #     query. 
    #     """

    relavent_files_template = f"""Instructions:
        - Your task is to identify the files and folders from the given directory structure that are most relevant to the user query.
        - Do not modify or alter any code in the provided files. Your responsibility is to extract the code relevant to the user query without changing it.
        - Provide the complete code of the identified files, along with their full paths, as they appear in the directory structure.
        - If a file or folder is relevant, make sure to include its full file path before the code snippet.
        - You are not required to directly answer the user's query. Your task is to help identify the specific files that are pertinent to the context and query.
        
        **User Query Context:**
        The user query is as follows:
        {user_query}
        
        **Codebase Directory Structure Context:**
        You will be given the following directory structure, which represents the file organization of the project:
        
        {code_base_context}
        
        **How to Provide the Output:**
        - For each relevant file, provide the complete code (as-is) within the code block.
        - Include the full file path before each code snippet. For example, the output should look like this:
            ```python
            # project_root/app/schemas/user.py
            
            from pydantic import BaseModel

            class UserLogin(BaseModel):
                username: str
                password: str

            class UserResponse(BaseModel):
                access_token: str
                token_type: str
            ```
        - Ensure that each file’s code appears exactly as it is in the codebase. Do not edit, alter, or summarize the code in any way.
        - If a file contains a function, class, or method that might be relevant to the user query, include it completely. This includes imports, variables, and any other code present in the file.
        
        **Important Notes:**
        - Identify files based on the **relevance** to the query provided. Some files may be important because they define core classes, functions, routes, models, or configurations.
        - If a file or folder is clearly unrelated to the query, do not include it.
        - Pay attention to the **path** of the files in the directory structure. When referencing code snippets, include the complete relative path to the file, starting from the root of the project folder.
        - In cases where a file has multiple sections that may seem relevant, provide the complete code in that file, unless it’s clearly not connected to the user query.
        - If you are unsure whether a file is relevant, provide as much context as possible by including those files that seem logically connected based on the structure and user query.

        Follow these guidelines carefully to ensure accurate identification of the files and correct inclusion of their code.

    """




    relavent_files = get_conversation_openai(template = relavent_files_template)



    # Specify the file name and path
    file_name = "relavant_files.txt"  # Writing to the root folder

    # Combine the base path with the file name to get the full path
    file_name = os.path.join(folder_path, file_name)

    # print(gen_code)

    # Write the string to the file
    try:
        with open(file_name, "w", encoding='utf-8') as file:
            file.write(relavent_files)
        print(f"Relavant files are saved successfully written to: {file_name}")
    except PermissionError:
        print("Permission denied: You need elevated privileges to write to the root folder.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # print(ans)


    code_editing_template = f"""
        You ara code editor who is editing the code of the file which is relevant to the user query given.

        The user query is as follows:

        {user_query}
        
        The code which you need to change is as follows:

        {relavent_files}

        Now you have to edit the code of the file which is relevant to the user query.

        for your reference the context of the code base is as follows:
        
        {code_base_context}

        Remember to add path before the  code snnipet. 
        For example:
            ```python
            # project_root/app/schemas/user.py

            from pydantic import BaseModel

            class UserLogin(BaseModel):
                username: str
                password: str

            class UserResponse(BaseModel):
                access_token: str
                token_type: str
            ```
        """

    edited_code = get_conversation_openai(template = code_editing_template)

    # Specify the file name and path
    file_name = "prompt_answer.txt"  # Writing to the root folder

    # Combine the base path with the file name to get the full path
    file_name = os.path.join(folder_path, file_name)

    # print(gen_code)

    print(edited_code)

    # Write the string to the file
    try:
        with open(file_name, "w", encoding='utf-8') as file:
            file.write(edited_code)
        print(f"Answer to you Query is successfully written to: {file_name}")
    except PermissionError:
        print("Permission denied: You need elevated privileges to write to the root folder.")
    except Exception as e:
        print(f"An error occurred: {e}")




