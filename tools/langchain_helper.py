from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain.vectorstores import FAISS

_template = """
Given the following conversation and a follow up question, 
rephrase the follow up question to be a standalone question, 
in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(_template)

def load_index_tools(documents_info):
    tools = []

    for tool_name, tool_info in documents_info.items():
        embeddings = OpenAIEmbeddings()
        index = FAISS.load_local(tool_info['save_path'], embeddings)
        retriever = index.as_retriever()

        tool = create_retriever_tool(
            retriever,
            tool_name,
            tool_info['description']
        )

        tools.append(tool)

    return tools


def vectordb_qa_with_memory(documents_info, temperature=0.3, model_name='gpt-3.5-turbo'):
    for tool_name, tool_info in documents_info.items():
        embeddings = OpenAIEmbeddings()
        vectordb = FAISS.load_local(tool_info['save_path'], embeddings)
        retriever = vectordb.as_retriever()
        model = ChatOpenAI(model_name=model_name, temperature=temperature)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        qa = ConversationalRetrievalChain.from_llm(
            model,
            retriever,
            condense_question_prompt=CUSTOM_QUESTION_PROMPT,
            memory=memory
        )

    return qa
