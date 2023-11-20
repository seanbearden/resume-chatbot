from langchain.agents import AgentExecutor
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.prompts import MessagesPlaceholder
from langchain.schema.messages import SystemMessage
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os.path
from tools import create_nested_directory


def load_index_tools(documents_info, repo_path=None):
    tools = []
    for tool_name, tool_info in documents_info.items():
        embeddings = OpenAIEmbeddings()
        if repo_path:
            vectordb = FAISS.load_local(os.path.join(repo_path, tool_info['save_path']), embeddings)
        else:
            vectordb = FAISS.load_local(tool_info['save_path'], embeddings)
        retriever = vectordb.as_retriever()

        tool = create_retriever_tool(
            retriever,
            tool_name,
            tool_info['description']
        )
        tools.append(tool)

    return tools


def vectordb_agent_executor_with_memory(documents_info, system_message_prompt, memory_key="chat_history",
                                        temperature=0.3, repo_path=None,
                                        model_name='gpt-3.5-turbo', verbose=False, user_uuid="DEFAULT",
                                        output_key='output'):
    # Load the language model
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    # set up memory
    message_history = DynamoDBChatMessageHistory(table_name="SessionTable", session_id=user_uuid)
    memory = ConversationBufferMemory(
        memory_key=memory_key, chat_memory=message_history, output_key=output_key, return_messages=True,

    )

    system_message = SystemMessage(content=(system_message_prompt))

    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
    )

    tools = load_index_tools(documents_info, repo_path=repo_path)

    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=verbose,
                                   return_intermediate_steps=True)
    return agent_executor


def create_vector_stores(documents_info, text_only=False):
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
