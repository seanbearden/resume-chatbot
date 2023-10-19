from dotenv import load_dotenv
from flask import session
from fast_dash import FastDash, dcc, dmc, Chat
# from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
# from langchain.chat_models import ChatOpenAI
# from langchain.memory import ConversationBufferMemory

import os
from tools import load_dict_from_json, load_index_tools, vectordb_qa_with_memory


# load API keys
load_dotenv()

documents_info_path = 'res/data/documents_info.json'
documents_info = load_dict_from_json(documents_info_path)

qa = vectordb_qa_with_memory(documents_info, temperature=0.3, model_name='gpt-3.5-turbo')

# tools = load_index_tools(documents_info)

# llm = ChatOpenAI(temperature=0.1)

# agent_executor = create_conversational_retrieval_agent(llm, tools, verbose=False)


# Define components

query_component = dmc.Textarea(
    placeholder="Write your query here",
    autosize=True,
    minRows=4,
    required=True,
    description="Write your query here",
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
        result = qa({"question": query, "chat_history": chat_history})
        answer = result["answer"]
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
