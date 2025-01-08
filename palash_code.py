# working but need to tell in question to create nrew file 

# import os
# import re
# from langchain_google_genai import ChatGoogleGenerativeAI

# # Set your API key

# # Initialize the ChatGoogleGenerativeAI with your model
# llm = ChatGoogleGenerativeAI(model="gemini-pro")

# # Simple in-memory storage for user sessions
# user_sessions = {}

# def create_codebase_structure(folder_name):
#     """Create a base project structure."""
#     os.makedirs(folder_name, exist_ok=True)
#     print(f"Codebase structure '{folder_name}' created successfully.")

# def determine_filename(base_dir, question):
#     """Generate a new filename based on the question or use existing if appropriate."""
#     # Check for specific task-related words to create different files
#     if "registration" in question.lower():
#         return os.path.join(base_dir, "registration_api.py")
#     elif "login" in question.lower():
#         return os.path.join(base_dir, "login_api.py")
#     elif "database" in question.lower():
#         return os.path.join(base_dir, "database_setup.py")
#     else:
#         # Default file if no specific task is detected
#         return os.path.join(base_dir, "main_code.py")

# def generate_code(user_id, question):
#     """Generate code based on user input and previous context."""
#     # Check if this is the first question from the user
#     if user_id not in user_sessions:
#         # Create a new project structure based on the user's input
#         folder_name = question.split("create a codebase structure")[-1].strip() or "my_project"
#         create_codebase_structure(folder_name)
#         user_sessions[user_id] = {"base_dir": folder_name, "questions": [question]}  # Store base dir and questions
#         print(f"Codebase created for {user_id}")
#         return
#     else:
#         user_sessions[user_id]["questions"].append(question)

#     # Get the user's base directory from the session
#     base_dir = user_sessions[user_id]["base_dir"]

#     # Generate a prompt for the model, including past questions for context
#     previous_questions = " ".join(user_sessions[user_id]["questions"])
#     prompt = (
#         f"You are a code generator. The user has previously asked: '{previous_questions}'. "
#         f"Now they ask: '{question}'. Generate appropriate Python code based on this context, "
#         f"and decide whether to add it to an existing file or create a new one if needed."
#     )

#     # Get the code from Google Gemini model
#     response = llm.invoke(prompt)

#     # Extract the code from the response
#     if hasattr(response, 'content'):
#         code = response.content.strip()  # Adjust if the response structure differs
#     else:
#         print("Error: Unexpected response format from the model.")
#         return

#     # Determine the filename to write code to
#     filename = determine_filename(base_dir, question)
    
#     # Append or create the new code file
#     with open(filename, "a") as f:
#         f.write(f"\n# Code Block for: {question}\n")
#         f.write(code + "\n")  # Write the generated code

#     print(f"Code generated and saved to '{filename}'.")

# def main():
#     user_id = input("Enter your user ID: ")
    
#     while True:
#         question = input("What do you want to do? (Type 'exit' to quit) ")
#         if question.lower() == 'exit':
#             break
#         generate_code(user_id, question)

# if __name__ == "__main__":
#     main()








# working best with vectorizer for keyword naming 

"""When a user asks a question, the TfidfVectorizer helps your program figure out which keywords to use for naming the file where the generated code will be saved. This makes the code more organized and relevant to what the user is asking.
"""


# import os
# import re
# from langchain_google_genai import ChatGoogleGenerativeAI
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Set your API key

# # Initialize the ChatGoogleGenerativeAI with your model
# llm = ChatGoogleGenerativeAI(model="gemini-pro")

# # Simple in-memory storage for user sessions
# user_sessions = {}

# def create_codebase_structure(folder_name):
#     """Create a base project structure."""
#     os.makedirs(folder_name, exist_ok=True)
#     print(f"Codebase structure '{folder_name}' created successfully.")

# def extract_keywords(question):
#     """Extract keywords dynamically using TF-IDF and regex."""
#     # Predefined generic corpus for backend terms
#     backend_terms = [
#         "login", "authentication", "authorization", "registration", "user", "admin",
#         "payment", "order", "product", "database", "api", "service"
#     ]
    
#     # Append the question to the corpus to analyze its keywords
#     corpus = backend_terms + [question]
    
#     # Use TF-IDF to identify terms in the question that match backend terminology
#     vectorizer = TfidfVectorizer(stop_words='english', max_features=3)
#     tfidf_matrix = vectorizer.fit_transform(corpus)
#     feature_names = vectorizer.get_feature_names_out()
    
#     question_keywords = [
#         feature for feature in feature_names
#         if feature in question.lower()
#     ]
    
#     # Default to "misc" if no strong keywords are found
#     return question_keywords or ["misc"]

# def determine_filename(base_dir, question, generated_code):
#     """Determine the filename based on extracted keywords or default to a generic name."""
#     # Extract keywords from the question
#     keywords = extract_keywords(question)
    
#     # Generate filename based on keywords
#     if "misc" in keywords:
#         filename = "misc_functionality.py"
#     else:
#         filename = f"{'_'.join(keywords)}.py"
    
#     # Ensure unique filename by appending a counter if file already exists
#     counter = 1
#     base_filename = os.path.splitext(filename)[0]
#     while os.path.exists(os.path.join(base_dir, filename)):
#         filename = f"{base_filename}_{counter}.py"
#         counter += 1

#     return os.path.join(base_dir, filename)

# def generate_code(user_id, question):
#     """Generate code based on user input and previous context."""
#     # If this is the first question from the user, create a new project structure
#     if user_id not in user_sessions:
#         folder_name = question.split("create a codebase structure")[-1].strip() or "my_project"
#         create_codebase_structure(folder_name)
#         user_sessions[user_id] = {"base_dir": folder_name, "questions": [question]}
#         print(f"Codebase created for {user_id}")
#         return
#     else:
#         user_sessions[user_id]["questions"].append(question)

#     # Get the user's base directory from the session
#     base_dir = user_sessions[user_id]["base_dir"]

#     # Generate a prompt for the model, including past questions for context
#     previous_questions = " ".join(user_sessions[user_id]["questions"])
#     prompt = (
#         f"You are a code generator like chatgpt and google bard. The user has previously asked: '{previous_questions}'. "
#         f"Now they ask: '{question}'. Generate appropriate Python code and files required to fullfill based on this context, "
#         f"and decide whether to add it to an existing file or create a new one if needed."
#     )




#     # Get the code from Google Gemini model
#     response = llm.invoke(prompt)

#     # Extract the code from the response
#     if hasattr(response, 'content'):
#         code = response.content.strip()
#     else:
#         print("Error: Unexpected response format from the model.")
#         return

#     # Determine the filename based on the generated code or question
#     filename = determine_filename(base_dir, question, code)
    
#     # Write the new code to the determined file
#     with open(filename, "a") as f:
#         f.write(f"\n# Code Block for: {question}\n")
#         f.write(code + "\n")

#     print(f"Code generated and saved to '{filename}'.")

# def main():
#     user_id = input("Enter your user ID: ")
    
#     while True:
#         question = input("What do you want to do? (Type 'exit' to quit) ")
#         if question.lower() == 'exit':
#             break
#         generate_code(user_id, question)

# if __name__ == "__main__":
#     main()










# final gemini use this only

# import os
# import re
# from langchain_google_genai import ChatGoogleGenerativeAI
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Set your API key

# # Initialize the ChatGoogleGenerativeAI with your model
# llm = ChatGoogleGenerativeAI(model="gemini-pro")

# # Simple in-memory storage for user sessions
# user_sessions = {}

# def create_codebase_structure(folder_name):
#     """Create a base project structure."""
#     os.makedirs(folder_name, exist_ok=True)
#     print(f"Codebase structure '{folder_name}' created successfully.")

# def extract_keywords(question):
#     """Extract keywords dynamically using TF-IDF and regex."""
#     # Predefined generic corpus for backend terms
#     backend_terms = [
#         "login", "authentication", "authorization", "registration", "user", "admin",
#         "payment", "order", "product", "database", "api", "service"
#     ]
    
#     # Append the question to the corpus to analyze its keywords
#     corpus = backend_terms + [question]
    
#     # Use TF-IDF to identify terms in the question that match backend terminology
#     vectorizer = TfidfVectorizer(stop_words='english', max_features=3)
#     tfidf_matrix = vectorizer.fit_transform(corpus)
#     feature_names = vectorizer.get_feature_names_out()
    
#     question_keywords = [
#         feature for feature in feature_names
#         if feature in question.lower()
#     ]
    
#     # Default to "misc" if no strong keywords are found
#     return question_keywords or ["misc"]

# def determine_filename(base_dir, question, generated_code):
#     """Determine the filename based on extracted keywords or default to a generic name."""
#     # Extract keywords from the question
#     keywords = extract_keywords(question)
    
#     # Generate filename based on keywords
#     if "misc" in keywords:
#         filename = "misc_functionality.py"
#     else:
#         filename = f"{'_'.join(keywords)}.py"
    
#     # Ensure unique filename by appending a counter if file already exists
#     counter = 1
#     base_filename = os.path.splitext(filename)[0]
#     while os.path.exists(os.path.join(base_dir, filename)):
#         filename = f"{base_filename}_{counter}.py"
#         counter += 1

#     return os.path.join(base_dir, filename)

# def generate_code(user_id, question):
#     """Generate code based on user input and previous context."""
#     # If this is the first question from the user, create a new project structure
#     if user_id not in user_sessions:
#         folder_name = question.split("create a codebase structure")[-1].strip() or "my_project"
#         create_codebase_structure(folder_name)
#         user_sessions[user_id] = {"base_dir": folder_name, "questions": [question]}
#         print(f"Codebase created for {user_id}")
#         return
#     else:
#         user_sessions[user_id]["questions"].append(question)

#     # Get the user's base directory from the session
#     base_dir = user_sessions[user_id]["base_dir"]

#     # Generate a prompt for the model, including past questions for context
#     previous_questions = " ".join(user_sessions[user_id]["questions"])
#     prompt = (
#         f"You are a code generator like chatgpt and google bard. The user has previously asked: '{previous_questions}'. "
#         f"Now they ask: '{question}'. Generate appropriate Python code and files required to fullfill based on this context, "
#         f"and decide whether to add it to an existing file or create a new one if needed."
#         f"Comment out the text which are not considered as a code comment every normal text except code."
#     )


#     # Get the code from Google Gemini model
#     response = llm.invoke(prompt)

#     # Extract the code from the response
#     if hasattr(response, 'content'):
#         code = response.content.strip()
#     else:
#         print("Error: Unexpected response format from the model.")
#         return

#     # Determine the filename based on the generated code or question
#     filename = determine_filename(base_dir, question, code)
    
#     # Write the new code to the determined file
#     with open(filename, "a") as f:
#         f.write(f"\n# Code Block for: {question}\n")
#         f.write(code + "\n")

#     print(f"Code generated and saved to '{filename}'.")

# def main():
#     user_id = input("Enter your user ID: ")
    
#     while True:
#         question = input("What do you want to do? (Type 'exit' to quit) ")
#         if question.lower() == 'exit':
#             break
#         generate_code(user_id, question)

# if __name__ == "__main__":
#     main()












# gemeni changes are done in the same file but different codes 

# import os
# import re
# from langchain_google_genai import ChatGoogleGenerativeAI
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Set your API key

# # Initialize the ChatGoogleGenerativeAI with your model
# llm = ChatGoogleGenerativeAI(model="gemini-pro")

# # Simple in-memory storage for user sessions
# user_sessions = {}

# def create_codebase_structure(folder_name):
#     """Create a base project structure."""
#     os.makedirs(folder_name, exist_ok=True)
#     print(f"Codebase structure '{folder_name}' created successfully.")

# def extract_keywords(question):
#     """Extract keywords dynamically using TF-IDF and regex."""
#     backend_terms = [
#         "login", "authentication", "authorization", "registration", "user", "admin",
#         "payment", "order", "product", "database", "api", "service"
#     ]
    
#     corpus = backend_terms + [question]
    
#     vectorizer = TfidfVectorizer(stop_words='english', max_features=3)
#     tfidf_matrix = vectorizer.fit_transform(corpus)
#     feature_names = vectorizer.get_feature_names_out()
    
#     question_keywords = [
#         feature for feature in feature_names
#         if feature in question.lower()
#     ]
    
#     return question_keywords or ["misc"]

# def determine_filename(base_dir, question):
#     """Determine the filename based on extracted keywords or default to a generic name."""
#     keywords = extract_keywords(question)
    
#     if "misc" in keywords:
#         filename = "misc_functionality.py"
#     else:
#         filename = f"{'_'.join(keywords)}.py"
    
#     return os.path.join(base_dir, filename)

# def modify_code(filename, old_line, new_line):
#     """Modify the existing code in the file."""
#     if os.path.exists(filename):
#         with open(filename, "r") as f:
#             code_lines = f.readlines()
        
#         # Replace old line with new line
#         code_lines = [line.replace(old_line, new_line) for line in code_lines]

#         with open(filename, "w") as f:
#             f.writelines(code_lines)
#         print(f"Code updated in '{filename}'.")
#     else:
#         print(f"Error: '{filename}' does not exist.")

# def generate_code(user_id, question):
#     """Generate or modify code based on user input."""
#     if user_id not in user_sessions:
#         folder_name = question.split("create a codebase structure")[-1].strip() or "my_project"
#         create_codebase_structure(folder_name)
#         user_sessions[user_id] = {"base_dir": folder_name, "questions": [question]}
#         print(f"Codebase created for {user_id}")
#         return
#     else:
#         user_sessions[user_id]["questions"].append(question)

#     base_dir = user_sessions[user_id]["base_dir"]
#     filename = determine_filename(base_dir, question)

#     # Check if the question indicates a modification
#     if "change" in question.lower():
#         # Extract the old and new strings from the question
#         parts = question.split("change")
#         if len(parts) >= 2:
#             old_line = parts[1].strip().split("to")[0].strip()  # Extract what to change
#             new_line = parts[1].strip().split("to")[1].strip()  # Extract new value
#             modify_code(filename, old_line, new_line)
#             return

#     # Generate a prompt for the model
#     previous_questions = " ".join(user_sessions[user_id]["questions"])
#     prompt = (
#         f"You are a code generator like chatgpt and google bard. The user has previously asked: '{previous_questions}'. "
#         f"Now they ask: '{question}'. Generate appropriate Python code and files required to fulfill based on this context."
#     )

#     response = llm.invoke(prompt)

#     if hasattr(response, 'content'):
#         code = response.content.strip()
#     else:
#         print("Error: Unexpected response format from the model.")
#         return

#     # Write the new code to the determined file
#     with open(filename, "a") as f:
#         f.write(f"\n# Code Block for: {question}\n")
#         f.write(code + "\n")

#     print(f"Code generated and saved to '{filename}'.")

# def main():
#     user_id = input("Enter your user ID: ")
    
#     while True:
#         question = input("What do you want to do? (Type 'exit' to quit) ")
#         if question.lower() == 'exit':
#             break
#         generate_code(user_id, question)

# if __name__ == "__main__":
#     main()







# working best making changes in the same file but 70-80% accuracy but not create multiple files for multiple dufferent question

# import os
# from langchain_google_genai import ChatGoogleGenerativeAI

# # Set your API key

# # Initialize the ChatGoogleGenerativeAI with your model
# llm = ChatGoogleGenerativeAI(model="gemini-pro")

# # Simple in-memory storage for user sessions
# user_sessions = {}

# def create_codebase_structure(folder_name):
#     """Create a base project structure."""
#     os.makedirs(folder_name, exist_ok=True)
#     print(f"Codebase structure '{folder_name}' created successfully.")

# def determine_filename(base_dir):
#     """Determine the filename for the main functionality."""
#     return os.path.join(base_dir, "misc_functionality.py")

# def replace_code(filename, old_string, new_string):
#     """Replace occurrences of old_string with new_string in the file."""
#     if os.path.exists(filename):
#         with open(filename, "r") as f:
#             code_lines = f.readlines()
        
#         # Track if any replacements were made
#         modified = False
        
#         # Replace old string with new string in all lines
#         updated_code = []
#         for line in code_lines:
#             if old_string in line:
#                 modified = True
#                 line = line.replace(old_string, new_string)
#             updated_code.append(line)

#         # Write back to the file only if modifications were made
#         if modified:
#             with open(filename, "w") as f:
#                 f.writelines(updated_code)
#             print(f"Code updated in '{filename}'.")
#         else:
#             print(f"No occurrences of '{old_string}' found in '{filename}'.")
#     else:
#         print(f"Error: '{filename}' does not exist.")

# def generate_code(user_id, question):
#     """Generate or modify code based on user input."""
#     if user_id not in user_sessions:
#         folder_name = question.split("create a codebase structure")[-1].strip() or "my_project"
#         create_codebase_structure(folder_name)
#         user_sessions[user_id] = {"base_dir": folder_name, "questions": [question]}
#         print(f"Codebase created for {user_id}")
#         return
#     else:
#         user_sessions[user_id]["questions"].append(question)

#     base_dir = user_sessions[user_id]["base_dir"]
#     filename = determine_filename(base_dir)

#     # Check if the question indicates a modification
#     if "change" in question.lower():
#         # Extract the old and new strings from the question
#         if "to" in question:
#             parts = question.split("to")
#             if len(parts) >= 2:
#                 old_string = parts[0].split("change")[-1].strip()  # Extract what to change
#                 new_string = parts[1].strip()  # Extract new value
#                 replace_code(filename, old_string, new_string)
#                 return

#     # Generate new function based on user input
#     prompt = (
#         f"You are a code generator. The user asked: '{question}'. "
#         f"Generate appropriate Python code to fulfill this request."
#     )

#     response = llm.invoke(prompt)

#     if hasattr(response, 'content'):
#         code = response.content.strip()
#     else:
#         print("Error: Unexpected response format from the model.")
#         return

#     # Write the generated code to the determined file
#     with open(filename, "w") as f:
#         f.write(f"# Code Block for: {question}\n")
#         f.write(code + "\n")

#     print(f"Code generated and saved to '{filename}'.")

# def main():
#     user_id = input("Enter your user ID: ")
    
#     while True:
#         question = input("What do you want to do? (Type 'exit' to quit) ")
#         if question.lower() == 'exit':
#             break
#         generate_code(user_id, question)

# if __name__ == "__main__":
#     main()








# looking for multiple file creations with different questions and same file changes if similar kind of question 

import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Set your API key

# Initialize the ChatGoogleGenerativeAI with your model
llm = ChatGoogleGenerativeAI(model="gemini-pro")

# Simple in-memory storage for user sessions
user_sessions = {}

def create_codebase_structure(folder_name):
    """Create a base project structure."""
    os.makedirs(folder_name, exist_ok=True)
    print(f"Codebase structure '{folder_name}' created successfully.")

def determine_filename(base_dir, question):
    """Determine a unique filename based on the question."""
    file_base_name = "_".join(question.split())[:20]  # Limit name length for readability
    filename = os.path.join(base_dir, f"{file_base_name}.py")
    count = 1
    while os.path.exists(filename):
        filename = os.path.join(base_dir, f"{file_base_name}_{count}.py")
        count += 1
    return filename

def replace_code(filename, old_string, new_string):
    """Replace occurrences of old_string with new_string in the file."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            code_lines = f.readlines()
        
        # Track if any replacements were made
        modified = False
        
        # Replace old string with new string in all lines
        updated_code = []
        for line in code_lines:
            if old_string in line:
                modified = True
                line = line.replace(old_string, new_string)
            updated_code.append(line)

        # Write back to the file only if modifications were made
        if modified:
            with open(filename, "w") as f:
                f.writelines(updated_code)
            print(f"Code updated in '{filename}'.")
        else:
            print(f"No occurrences of '{old_string}' found in '{filename}'.")
    else:
        print(f"Error: '{filename}' does not exist.")

def generate_code(user_id, question):
    """Generate or modify code based on user input."""
    if user_id not in user_sessions:
        folder_name = question.split("create a codebase structure")[-1].strip() or "my_project"
        create_codebase_structure(folder_name)
        user_sessions[user_id] = {"base_dir": folder_name, "files": {}}
        print(f"Codebase created for {user_id}")
    
    base_dir = user_sessions[user_id]["base_dir"]
    specified_filename = None

    # Check if the question specifies a filename
    if "in" in question.lower():
        specified_filename = question.split("in")[-1].strip().split()[0]

    if specified_filename:
        filename = os.path.join(base_dir, f"{specified_filename}.py")
    else:
        # Generate a new file if the question isn't related to an existing file
        filename = determine_filename(base_dir, question)
        
    # Check if the question indicates a modification
    if "change" in question.lower() and specified_filename:
        if "to" in question:
            parts = question.split("to")
            if len(parts) >= 2:
                old_string = parts[0].split("change")[-1].strip()
                new_string = parts[1].strip()
                replace_code(filename, old_string, new_string)
                return

    # Generate new function based on user input
    prompt = (
        f"You are a code generator. The user asked: '{question}'. "
        f"Generate appropriate Python code to fulfill this request."
    )

    response = llm.invoke(prompt)

    if hasattr(response, 'content'):
        code = response.content.strip()
    else:
        print("Error: Unexpected response format from the model.")
        return

    # Write the generated code to the determined file
    with open(filename, "w") as f:
        f.write(f"# Code Block for: {question}\n")
        f.write(code + "\n")

    print(f"Code generated and saved to '{filename}'.")

def main():
    user_id = input("Enter your user ID: ")
    
    while True:
        question = input("What do you want to do? (Type 'exit' to quit) ")
        if question.lower() == 'exit':
            break
        generate_code(user_id, question)

if __name__ == "__main__":
    main()








# looking for new foldwer creation , new folder is getting cretad 


# import os
# from langchain_google_genai import ChatGoogleGenerativeAI

# # Set your API key

# # Initialize the ChatGoogleGenerativeAI with your model
# llm = ChatGoogleGenerativeAI(model="gemini-pro")

# # Simple in-memory storage for user sessions
# user_sessions = {}

# def create_folder(base_dir, folder_name):
#     """Directly create a folder without generating any code file."""
#     folder_path = os.path.join(base_dir, folder_name)
#     os.makedirs(folder_path, exist_ok=True)
#     print(f"Folder '{folder_path}' created successfully.")
#     return folder_path

# def generate_code(user_id, question):
#     """Generate code or handle direct folder creation based on user input."""
#     if user_id not in user_sessions:
#         user_sessions[user_id] = {"base_dir": "codebase", "files": {}}
#         os.makedirs(user_sessions[user_id]["base_dir"], exist_ok=True)
    
#     base_dir = user_sessions[user_id]["base_dir"]

#     # Check for folder creation request
#     if "create a folder" in question.lower() or "create a new folder" in question.lower():
#         folder_name = question.split("with name")[-1].strip()
#         create_folder(base_dir, folder_name)
#         return  # Skip code generation for folder creation

#     # Determine filename for general code requests
#     filename = os.path.join(base_dir, "_".join(question.split())[:20] + ".py")

#     # Generate new code based on user input
#     prompt = (
#         f"You are a code generator. The user asked: '{question}'. "
#         f"Generate appropriate Python code to fulfill this request."
#     )

#     response = llm.invoke(prompt)

#     if hasattr(response, 'content'):
#         code = response.content.strip()
#     else:
#         print("Error: Unexpected response format from the model.")
#         return

#     # Write the generated code to the determined file
#     with open(filename, "w") as f:
#         f.write(f"# Code Block for: {question}\n")
#         f.write(code + "\n")

#     print(f"Code generated and saved to '{filename}'.")

# def main():
#     user_id = input("Enter your user ID: ")
    
#     while True:
#         question = input("What do you want to do? (Type 'exit' to quit) ")
#         if question.lower() == 'exit':
#             break
#         generate_code(user_id, question)

# if __name__ == "__main__":
#     main()






import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Set your API key

# Initialize the ChatGoogleGenerativeAI with your model
llm = ChatGoogleGenerativeAI(model="gemini-pro")

# Simple in-memory storage for user sessions
user_sessions = {}

def create_codebase_structure(folder_name):
    """Create a base project structure."""
    os.makedirs(folder_name, exist_ok=True)
    print(f"Codebase structure '{folder_name}' created successfully.")

def determine_filename(base_dir, question):
    """Determine a unique filename based on the question."""
    file_base_name = "_".join(question.split())[:20]  # Limit name length for readability
    filename = os.path.join(base_dir, f"{file_base_name}.py")
    count = 1
    while os.path.exists(filename):
        filename = os.path.join(base_dir, f"{file_base_name}_{count}.py")
        count += 1
    return filename

def replace_code(filename, old_string, new_string):
    """Replace occurrences of old_string with new_string in the file."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            code_lines = f.readlines()
        
        # Track if any replacements were made
        modified = False
        
        # Replace old string with new string in all lines
        updated_code = []
        for line in code_lines:
            if old_string in line:
                modified = True
                line = line.replace(old_string, new_string)
            updated_code.append(line)

        # Write back to the file only if modifications were made
        if modified:
            with open(filename, "w") as f:
                f.writelines(updated_code)
            print(f"Code updated in '{filename}'.")
        else:
            print(f"No occurrences of '{old_string}' found in '{filename}'.")
    else:
        print(f"Error: '{filename}' does not exist.")

def generate_code(user_id, question):
    """Generate or modify code based on user input."""
    if user_id not in user_sessions:
        folder_name = question.split("create a codebase structure")[-1].strip() or "my_project"
        create_codebase_structure(folder_name)
        user_sessions[user_id] = {"base_dir": folder_name, "files": {}}
        print(f"Codebase created for {user_id}")
        return  # Exit after creating the folder, do not generate a file
    
    base_dir = user_sessions[user_id]["base_dir"]
    specified_filename = None

    # Check if the question specifies a filename
    if "in" in question.lower():
        specified_filename = question.split("in")[-1].strip().split()[0]

    if specified_filename:
        filename = os.path.join(base_dir, f"{specified_filename}.py")
    else:
        # Generate a new file if the question isn't related to an existing file
        filename = determine_filename(base_dir, question)
        
    # Check if the question indicates a modification
    if "change" in question.lower() and specified_filename:
        if "to" in question:
            parts = question.split("to")
            if len(parts) >= 2:
                old_string = parts[0].split("change")[-1].strip()
                new_string = parts[1].strip()
                replace_code(filename, old_string, new_string)
                return

    # Generate new function based on user input
    prompt = (
        f"You are a code generator. The user asked: '{question}'. "
        f"Generate appropriate Python code to fulfill this request."
    )

    response = llm.invoke(prompt)

    if hasattr(response, 'content'):
        code = response.content.strip()
    else:
        print("Error: Unexpected response format from the model.")
        return

    # Write the generated code to the determined file
    with open(filename, "w") as f:
        f.write(f"# Code Block for: {question}\n")
        f.write(code + "\n")

    print(f"Code generated and saved to '{filename}'.")

def main():
    user_id = input("Enter your user ID: ")
    
    while True:
        question = input("What do you want to do? (Type 'exit' to quit) ")
        if question.lower() == 'exit':
            break
        generate_code(user_id, question)

if __name__ == "__main__":
    main()