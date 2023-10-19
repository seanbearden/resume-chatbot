from dotenv import load_dotenv
from flask import session
from fast_dash import FastDash, dcc, dmc, Chat
# from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
# from langchain.chat_models import ChatOpenAI
# from langchain.memory import ConversationBufferMemory

import os
from tools import load_dict_from_json, load_index_tools, vectordb_agent_executor_with_memory


# load API keys
load_dotenv()
name = "Sean Bearden"
documents_info_path = 'res/data/documents_info.json'
documents_info = load_dict_from_json(documents_info_path)
system_message_prompt = f"""Do your best to answer the questions asked about {name}. 
You have permission to use any tools available to look up relevant information, which will be necessary.
Assume you are conversing with a recruiter or hiring agent. Be helpful, but do not lie or embellish.
Your purpose is to assist {name} in getting hired for the right job.
"""

memory_key = "history"
agent_executor = vectordb_agent_executor_with_memory(documents_info, system_message_prompt, memory_key=memory_key,
                                                     temperature=0.3,
                                                     model_name='gpt-3.5-turbo', verbose=True)

# Define components

query_component = dmc.Textarea(
    placeholder=f"Write your query about {name} here",
    autosize=True,
    minRows=4,
    required=True,
    description=f"Ask anything about {name}",
)

answer_component = dcc.Markdown(
    style={"text-align": "left", "padding": "1%"}, link_target="_blank"
)


def ask_the_resume_chatbot(
        query: query_component,
) -> Chat:
    """
    Ask questions about Sean Bearden's qualification and experience. You can ask about his education and research,
    or his work experience.
    """
    answer_suffix = 'Visit SeanBearden.com for more information.'

    if not query:
        answer = "Did you forget writing your query in the query box?"

    else:
        # Get chat history from Flask session
        chat_history = session.get("chat_history", [])

        # Generate a response
        # result = agent({"question": query, memory_key: chat_history})
        result = agent_executor({"input": query})
        answer = result["output"]
        # Save chat history back to the session cache
        chat_history.append([query, answer])

        session["chat_history"] = chat_history

        answer = f"""{answer}

        {answer_suffix}
        """

    chat = dict(query=query, response=answer)

    return chat


# Build app (this is all it takes!). Fast Dash understands what it needs to do.
app = FastDash(
    ask_the_resume_chatbot,
    github_url=os.environ["GITHUB_URL"],
    linkedin_url=os.environ["LINKEDIN_URL"],
)
server = app.server
server.config["SECRET_KEY"] = "Some key"

if __name__ == "__main__":
    app.run()
