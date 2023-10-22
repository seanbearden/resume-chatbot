from langchain.agents import AgentExecutor
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
import os.path


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
                                        model_name='gpt-3.5-turbo', verbose=False):
    # Load the language model
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    # This is needed for both the memory and the prompt

    memory = AgentTokenBufferMemory(memory_key=memory_key, llm=llm)

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
