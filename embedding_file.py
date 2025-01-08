from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import openai
# from openai import Open
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = API_KEY

# text = ""
# file_path = r"C:\Users\Asus\Desktop\Code Files\Code_Generator\folder_content.txt"
# # Attempt to read the file content.
# try:
#     with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.read()  # Read the content of the file.
#             text += content  # Append the content to the text output.
# except Exception as e:
#         try:
#             with open(file_path, 'r', encoding='utf-16') as file:
#                 content = file.read()
#                 text += content  # Append the content to the text output.
#                         # print(content)
#         except Exception as e:
#                 print(f"Error reading file: {e}")

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create and save the FAISS vector store
def get_vector_store(text_chunks):
    # embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    print(embeddings)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
# Example usage:


def user_input(user_question):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    return docs

# text_chunks = get_text_chunks(text)
# get_vector_store(text_chunks)

user_ques = """I want to allow all of the origins in my middleware
"""

relavant_content = user_input(user_ques)

print(relavant_content)
