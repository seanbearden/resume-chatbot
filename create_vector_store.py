from dotenv import load_dotenv
import os
from tools import load_dict_from_json, create_vector_stores, get_parent_dir_path

# load API keys
load_dotenv()

text_only = False
current_dir = os.getcwd()
repo_path = get_parent_dir_path(current_dir, 'resume-chatbot')
documents_info_path = 'res/data/documents_info.json'
documents_info = load_dict_from_json(os.path.join(repo_path, documents_info_path))

create_vector_stores(documents_info, text_only=text_only)
