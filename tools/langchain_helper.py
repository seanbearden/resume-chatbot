from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS


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
