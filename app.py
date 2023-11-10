import boto3
from dotenv import load_dotenv
from flask import session, request
from fast_dash import FastDash, dcc, dmc, Chat
import time
from tools import load_dict_from_json, vectordb_agent_executor_with_memory, get_str_template

# load API keys
load_dotenv()

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChatbotTable')

temperature = 0.5
model_name = 'gpt-4-1106-preview'

template_kwargs_path = './res/templates/template_kwargs.json'
template_kwargs = load_dict_from_json(template_kwargs_path)
name = template_kwargs['name']
website = template_kwargs['website']

about_template_path = './res/templates/about.txt'
about_template = get_str_template(about_template_path)
about = about_template.substitute(**template_kwargs)

system_message_template_path = './res/templates/system_message_prompt.txt'
system_message_template = get_str_template(system_message_template_path)
system_message_prompt = system_message_template.substitute(**template_kwargs)

documents_info_path = './res/data/documents_info.json'
documents_info = load_dict_from_json(documents_info_path)

memory_key = "history"
agent_executor = vectordb_agent_executor_with_memory(documents_info, system_message_prompt, memory_key=memory_key,
                                                     temperature=temperature,
                                                     model_name=model_name, verbose=True)

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
    Ask questions about applicant's qualification and experience. (Using GPT-4 Turbo!)
    """

    timestamp = int(time.time())

    answer_suffix = f"Visit {website} for more information."

    if not query:
        answer = "Did you forget writing your query in the query box?"

    else:

        # Get chat history from Flask session
        # Tech Debt: need to pass chat history into agent.
        chat_history = session.get("chat_history", [])

        # Generate a response
        # result = agent({"question": query, memory_key: chat_history})
        result = agent_executor({"input": query})

        answer = result["output"]

        # Get IP address
        ip_address = request.remote_addr

        response = table.put_item(
            Item={
                'ip_address': ip_address,
                'timestamp': timestamp,  # You need to provide a value for the timestamp key
                "input": query,
                "output": answer
            }
        )

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
    github_url=template_kwargs.get("github_url", "https://github.com/"),
    linkedin_url=template_kwargs.get("linkedin_url", "https://www.linkedin.com/"),
    about=about
)
server = app.server
server.config["SECRET_KEY"] = "Some key"

if __name__ == "__main__":
    app.run()
