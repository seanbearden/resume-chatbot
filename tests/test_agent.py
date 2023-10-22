from dotenv import load_dotenv
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
from string import Template
from tools import load_dict_from_json, vectordb_agent_executor_with_memory, get_parent_dir_path
import unittest

load_dotenv()


class TestAgent(unittest.TestCase):

    def setUp(self) -> None:
        name = "Sean Bearden"
        current_dir = os.getcwd()
        repo_path = get_parent_dir_path(current_dir, 'resume-chatbot')
        documents_info_path = 'res/data/documents_info.json'
        documents_info = load_dict_from_json(os.path.join(repo_path, documents_info_path))
        temperature = 0.2
        self.tools = []
        for tool_name, tool_info in documents_info.items():
            embeddings = OpenAIEmbeddings()
            index = FAISS.load_local(os.path.join(repo_path, tool_info['save_path']), embeddings)
            retriever = index.as_retriever()

            tool = create_retriever_tool(
                retriever,
                tool_name,
                tool_info['description']
            )

            self.tools.append(tool)

        with open(os.path.join(repo_path, 'res/templates/system_message_prompt.txt'), 'r') as file:
            # Read the contents of the file into a string variable
            system_message_template = Template(file.read())

        system_message_prompt = system_message_template.substitute(name=name)

        self.agent_executor = vectordb_agent_executor_with_memory(
            documents_info, system_message_prompt,
            temperature=temperature, repo_path=repo_path,
            model_name='gpt-3.5-turbo-16k', verbose=False)

    def test_agent_knowledge_of_applicant(self):
        result = self.agent_executor({"input": "Tell me about Sean Bearden"})
        output = result["output"].lower()
        # Test knowledge of name
        self.assertTrue("bearden" in output)
        # Test knowledge of expertise
        self.assertTrue("physics" in output)

    def test_agent_personal_interests(self):
        result = self.agent_executor({"input": "What are some of Sean's interests outside of work?"})
        output = result["output"].lower()
        # Test knowledge of activities
        self.assertTrue("yoga" in output)
        # Test knowledge of technical interests
        self.assertTrue("large language model" in output)
