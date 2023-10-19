from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader
from tools import load_dict_from_json, create_nested_directory

# load API keys
load_dotenv()

text_only = False

documents_info_path = 'res/data/documents_info.json'
documents_info = load_dict_from_json(documents_info_path)

for tool_name, tool_info in documents_info.items():
    if text_only:
        loader = DirectoryLoader(tool_info['directory_path'], glob="**/*.txt", loader_cls=TextLoader)
    else:
        loader = DirectoryLoader(tool_info['directory_path'])

    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)
    path = tool_info['save_path']
    create_nested_directory(path)
    db.save_local(path)
