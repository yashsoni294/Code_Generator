import os
import openai
import re
from dotenv import load_dotenv
import openai
import tkinter as tk
from docx import Document

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
# openai.api_key = ""


def replace_braces(input_string):
    """
    Replaces all occurrences of '{' with '[' and '}' with ']' in the input string.
    
    Parameters:
        input_string (str): The string to process.
        
    Returns:
        str: The modified string with replacements.
    """
    return input_string.replace('{', '[').replace('}', ']')


# def get_conversation_openai(template, model="gpt-4o-mini", temperature=0.01, max_tokens=None, presence_penalty=0.0, frequency_penalty=0.0):
#     """
#     Interacts with the OpenAI model based on a provided template.
    
#     Args:
#         template (str): A string template for generating prompts dynamically.
#         model (str, optional): The name of the OpenAI model to use. Defaults to "gpt-4o-mini".
#         temperature (float, optional): Sampling temperature. Defaults to 0.1.
#         max_tokens (int, optional): Maximum tokens for the response. Defaults to None.
#         presence_penalty (float, optional): Presence penalty parameter for the model. Defaults to 0.0.
#         frequency_penalty (float, optional): Frequency penalty parameter for the model. Defaults to 0.0.

#     Returns:
#         str: The content of the response generated by the OpenAI model.
#     """

#     try:
#         # Call the OpenAI Chat API to generate a response
#         response = openai.ChatCompletion.create(
#             model=model,
#             messages=[{"role": "system", "content": template}],
#             temperature=temperature,
#             max_tokens=max_tokens,
#             presence_penalty=presence_penalty,
#             frequency_penalty=frequency_penalty
#         )

#         # Log the API response

#         # Extract and return the content of the response
#         return response["choices"][0]["message"]["content"]
#     except Exception as e:
#         return "Error generating response"

def get_conversation_openai(template, model="gpt-4o-mini", temperature=0.01, max_tokens=None, presence_penalty=0.0, frequency_penalty=0.0):
    """
    Interacts with the OpenAI model based on a provided template.

    Args:
        template (str): A string template for generating prompts dynamically.
        model (str, optional): The name of the OpenAI model to use. Defaults to "gpt-4".
        temperature (float, optional): Sampling temperature. Defaults to 0.01.
        max_tokens (int, optional): Maximum tokens for the response. Defaults to None.
        presence_penalty (float, optional): Presence penalty parameter for the model. Defaults to 0.0.
        frequency_penalty (float, optional): Frequency penalty parameter for the model. Defaults to 0.0.

    Returns:
        str: The content of the response generated by the OpenAI model.
    """

    try:
        # Call the OpenAI Chat API to generate a response
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": template}],
            temperature=temperature,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty
        )

        # Extract and return the content of the response
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

        
class CustomDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Input")
        self.label = tk.Label(self.top, text="Enter the user story and acceptance criteria:")
        self.label.pack(pady=10)
        self.text = tk.Text(self.top, width=80, height=20)
        self.text.pack(pady=10)
        self.submit_button = tk.Button(self.top, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=10)
        self.result = None

    def on_submit(self):
        self.result = self.text.get("1.0", "end-1c")
        self.top.destroy()

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
        return self.result
    

base_path = input("Please Enter the base or folder path: ")

root = tk.Tk()
root.withdraw()  # Hide the main window

custom_dialog = CustomDialog(root)
user_story_accpt_criet = custom_dialog.show()
root.destroy()

frame_work = None

# Continue asking for input until a valid choice is entered (1 or 2)
while frame_work not in [1, 2]:
    try:
        frame_work = int(input("Please enter the number for respective framework : \n1. FastAPI \n2. Django.\n"))
        if frame_work not in [1, 2]:
            print("Invalid input. Please enter 1 or 2.")
    except ValueError:
        print("Invalid input. Please enter a number.")

if frame_work == 1:
    print(f"You selected framework FastAPI.")
else:
    print(f"You selected framework Django.")


prompt_template = f"""
    Please provide the API contract for the following user story and acceptance criteria:

    {user_story_accpt_criet}

    The API contract should include the necessary endpoints, request/response formats, and any other relevant details.
    Remember do not rush to generate the code. Take your time to generate a detailed and good quality API contract.

"""

api_contract = get_conversation_openai(template = prompt_template)


# Specify the file name
file_name = "gen_api_contract.docx"  # Ensure you have permissions to write to the root folder

# Combine the base path with the file name to get the full path
full_path = os.path.join(base_path, file_name)

# Create a new Word document
doc = Document()

# Add the API contract content to the document
doc.add_paragraph(api_contract)  # Make sure api_contract is defined

# Write the document to the .docx file
try:
    doc.save(full_path)
    print(f"Generated API contract successfully written to {full_path}")
except PermissionError:
    print("Permission denied: You need elevated privileges to write to the root folder.")
except Exception as e:
    print(f"An error occurred: {e}")

# # Write the string to the file
# try:
#     with open(full_path, "w", encoding='utf-8') as file:
#         file.write(api_contract)
#     print(f"API contract successfully written to {full_path}")
# except PermissionError:
#     print("Permission denied: You need elevated privileges to write to the root folder.")
# except Exception as e:
#     print(f"An error occurred: {e}")
    


prompt_template_django = f"""
    Remember do not rush to generate the code. Take your time to generate a detailed and good quality and error free 
    code. You are a Django Back-End code genrator that generates a detailed and good quality Django Back-End code and 
    the folder structure which we are using is as follows :

    structure = [
    "project_root": [
        "manage.py": None,
        "requirements.txt": None,
        ".env": None,
        ".gitignore": None,
        "README.md": None,
        "Dockerfile": None,
        "docker-compose.yml": None,
        "project_name": [
            "__init__.py": None,
            "asgi.py": None,
            "settings.py": None,
            "urls.py": None,
            "wsgi.py": None,
            "apps": [
                "app_name": [
                    "__init__.py": None,
                    "admin.py": None,
                    "apps.py": None,
                    "forms.py": None,
                    "models.py": None,
                    "urls.py": None,
                    "views.py": None,
                    "serializers.py": None,
                    "tasks.py": None,
                    "tests.py": None,
                    "signals.py": None,
                    "templates": [
                        "app_name": [
                            "*.html": None
                        ]
                    ],
                    "static": [
                        "css": None,
                        "js": None,
                        "images": None,
                        "fonts": None
                    ]
                ]
            ],
            "staticfiles": None
        ],
        "media": [
            "uploads": None
        ],
        "templates": [
            "base.html": None
        ],
        "static": [
            "css": None,
            "js": None,
            "images": None,
            "fonts": None
        ],
        "logs": [
            "django.log": None
        ],
        "scripts": [
            "manage_tasks.py": None
        ],
        "tests": [
            "__init__.py": None,
            "test_project.py": None
            ]
        ]
    ]
    
    Write a detailed and good quality Django Back-End code for the below user story and acceptance criteria:

    {user_story_accpt_criet}

    and its api contract should be as follows:

    {replace_braces(api_contract)}

    Remember to add path before the  code snnipet. Also the ``` before and after the code snnipet.
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
    
    Also create the code for the files and folders which you are Importing in the other files. For example Data Base,
    and Models folders etc.  Remember do not generate any unnecessary text or explanation. only generate detailed and
    good quality Django Back-End code. Also give the text which is necessary for the other files like requirements.txt, Dockerfile, 
    docker-compose.yml, README.md, .gitignore etc.
    """


prompt_template_fastapi = f"""
    Remember do not rush to generate the code. Take your time to generate a detailed and good quality and error free 
    code. You are a FastAPI Back-End code genrator that generate a detailed and good quality FastAPI Back-End code 
    and the folder structure which we are using is as follows :

    structure = [
    "project_root": [
        "app": [
            "api": [
                "__init__.py": None,
                "v1": [
                    "__init__.py": None,
                    "endpoints": [
                        "__init__.py": None,
                        "user.py": None,
                        "auth.py": None,
                        "other_endpoints.py": None,
                    ]
                ]
            ],
            "core": [
                "__init__.py": None,
                "config.py": None,
                "security.py": None,
                "dependencies.py": None,
            ],
            "models": [
                "__init__.py": None,
                "user.py": None,
                "other_models.py": None,
            ],
            "schemas": [
                "__init__.py": None,
                "user.py": None,
                "other_schemas.py": None,
            ],
            "crud": [
                "__init__.py": None,
                "user.py": None,
                "other_crud.py": None,
            ],
            "db": [
                "__init__.py": None,
                "base.py": None,
                "session.py": None,
                "migrations": "(Generated by Alembic)"
            ],
            "tests": [
                "__init__.py": None,
                "test_api": [
                    "__init__.py": None,
                    "test_user.py": None,
                    "test_auth.py": None,
                ]
            ],
            "main.py": None,
        ],
        "scripts": [
            "create_superuser.py": None,
            "initialize_db.py": None,
        ],
        "requirements.txt": None,
        ".env": None,
        ".env.example": None,
        "Dockerfile": None,
        "docker-compose.yml": None,
        "README.md": None,
        ".gitignore": None,
    ]]
    
    Write a detailed and good quality FastAPI Back-End code for the below user story and acceptance criteria:

    {user_story_accpt_criet}

    and its api contract should be as follows:

    {replace_braces(api_contract)}

    Remember to add path before the  code snnipet and also the ``` before and after the code snnipet. 
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
    
    Also create the code for the files and folders which you are Importing in the other files. For example Data Base,
    and Models folders etc.  Remember do not generate any unnecessary text or explanation. only generate detailed and
    good quality code. Also give the text which is necessary for the other files like requirements.txt, Dockerfile, 
    docker-compose.yml, README.md, .gitignore etc.
    """

if frame_work == 1:
    prompt_template = prompt_template_fastapi
else:
    prompt_template = prompt_template_django

gen_code = get_conversation_openai(template = prompt_template)


# Specify the file name and path
file_name = "gen_code.txt"  # Writing to the root folder

# Combine the base path with the file name to get the full path
full_path = os.path.join(base_path, file_name)

# print(gen_code)

# Write the string to the file
try:
    with open(full_path, "w", encoding='utf-8') as file:
        file.write(gen_code)
    print(f"API contract successfully written to: {full_path}")
except PermissionError:
    print("Permission denied: You need elevated privileges to write to the root folder.")
except Exception as e:
    print(f"An error occurred: {e}")



input_string = gen_code

# Regular expression to extract code snippets and their file paths
pattern = r"```(\w+)\n# (.+?)\n(.*?)```"

# Iterate through all matches in the input string
matches = re.finditer(pattern, input_string, re.DOTALL)

# Create files and write content
for match in matches:
    language = match.group(1)
    file_path = match.group(2).strip()
    # Combine the base path with the file name to get the full path
    file_path = os.path.join(base_path, file_path)
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
