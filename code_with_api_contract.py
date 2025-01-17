import os
from dotenv import load_dotenv
import openai
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = API_KEY

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
        logging.info("API response: %s", response)

        # Extract and return the content of the response
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error("Error during API call: %s", e)
        return "Error generating response"
    

def replace_braces(input_string):
    """
    Replaces all occurrences of '{' with '[' and '}' with ']' in the input string.
    
    Parameters:
        input_string (str): The string to process.
        
    Returns:
        str: The modified string with replacements.
    """
    return input_string.replace('{', '[').replace('}', ']')

# prompt = "Create a registration API using FastAPI that allows users to register with their email and password. The API should store the user data in a database and return a success message upon successful registration. Ensure that the API is secure and follows best practices for user authentication."        

# Specify the file path
file_name = "gen_api_contract.txt"

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



prompt = """Signup (parent and child)	Done	As a user, I want to  sign-up as parent or child so that I can create my credentials and gain access to the platform based on my user role.	1. User click on sign-up button with different options for parent and child
2. User is redirected to registration page
3. Once all required fields are filled and validated, clicking the 'Submit' or 'Sign-Up' button should register the user.
4. User can now login with created credentials
Login (parent and child)	Done	As a user, I want to login as parent and child so that user I can gain access platform based on my user role.	1. User click on login button with different options for parent and child
2. User is able to login the platform with existing credentials
3. Incorrect login attempts for either parent or child should display appropriate error messages.
3. User views the home screen
Forgot passcode	Done	As a user, I want to click on "Forgot Password" option to reset my password in case I forget it so that I can change my password and log in with a new password thereafter	1. User clicks on "Forgot Password"
2. Clicking on 'Forgot Password' should redirect the user to a password reset page/form
3. User is able to change existing password
4.. User is able to login with new password
Reset Password	Done	As a user, I want to click on "Reset Password" to reset my password at will so that I can login with new password thereafter.	1. User clicks on "Reset Password"
2. User is able to change existing password
3. User is able to login with new password

"""


prompt_template = f"""
    You are a code genrator that generte a detailed and good quality code and the folder structure which we are using 
    is as follows:

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
    
    Write a detailed and good quality code for the below input:

    {prompt}



    and its api contract should be as follows:

    {replace_braces(file_content)}

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
    
    Also create the files and folders which you are Importing in the other files. Remember do not generate any unnecessary text or explanation. only generate detailed and good quality code. Also give the text which is 
    necessary for the other files like requirements.txt, Dockerfile, docker-compose.yml, README.md, .gitignore etc.
    """
gen_code = get_conversation_openai(template = prompt_template)


import os

# Define the string
api_contract = "Your API contract content goes here."

# Specify the file name and path
file_name = "gen_code.txt"  # Writing to the root folder
full_path = os.path.abspath(file_name)

# Write the string to the file
try:
    with open(full_path, "w") as file:
        file.write(gen_code)
    print(f"API contract successfully written to: {full_path}")
except PermissionError:
    print("Permission denied: You need elevated privileges to write to the root folder.")
except Exception as e:
    print(f"An error occurred: {e}")


print(gen_code)
