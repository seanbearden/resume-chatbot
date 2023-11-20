import boto3
from datetime import datetime
from dotenv import load_dotenv
from dash import html
from flask import session, request
from fast_dash import FastDash, dcc, dmc, Chat
import os
import time
import uuid
from tools import load_dict_from_json, vectordb_agent_executor_with_memory, get_str_template

from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory

# load API keys
load_dotenv()

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SessionTable')

temperature = 0.5
model_name = 'gpt-4-1106-preview'

template_kwargs_path = './res/templates/template_kwargs.json'
template_kwargs = load_dict_from_json(template_kwargs_path)
name = template_kwargs['name']
website = template_kwargs['website']
answer_suffix = f"Visit {website} for more information."

about_template_path = './res/templates/about.txt'
about_template = get_str_template(about_template_path)
about = about_template.substitute(**template_kwargs)

system_message_template_path = './res/templates/system_message_prompt.txt'
system_message_template = get_str_template(system_message_template_path)
system_message_prompt = system_message_template.substitute(**template_kwargs)

documents_info_path = './res/data/documents_info.json'
documents_info = load_dict_from_json(documents_info_path)

memory_key = "chat_history"
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

    # Check if UUID is in session, if not, create and store it
    if 'user_uuid' not in session:
        session['user_uuid'] = str(uuid.uuid4())

    if not query:
        answer = "Did you forget writing your query in the query box?"

    else:

        # Get chat history from DynamoDB
        user_uuid = session['user_uuid']

        message_history = DynamoDBChatMessageHistory(table_name="SessionTable", session_id=user_uuid)
        session_memory = ConversationBufferMemory(
            memory_key=memory_key, chat_memory=message_history, output_key='output', return_messages=True
        )
        agent_executor.memory = session_memory

        # Generate a response
        result = agent_executor({"input": query})

        timestamp = datetime.utcnow().isoformat()  # Current timestamp

        table.update_item(
            Key={'SessionId': user_uuid},
            UpdateExpression='SET LastUpdated = :val',
            ExpressionAttributeValues={':val': timestamp}
        )

        answer = result["output"]

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
# TODO: Only display when mobile detected.
app.layout_object.inputs.append(dmc.Alert('Scroll down to see response if using mobile device.'))

server = app.server
server.config["SECRET_KEY"] = os.environ['FLASK_SECRET_KEY']

if __name__ == "__main__":
    app.run()
