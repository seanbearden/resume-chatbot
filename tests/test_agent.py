from dotenv import load_dotenv
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from tools.json_helper import load_dict_from_json
import unittest

load_dotenv()


class TestAgent(unittest.TestCase):

    def setUp(self) -> None:
        self.documents_info_path = 'res/data/documents_info.json'
        self.documents_info = load_dict_from_json(self.documents_info_path)

    def test_agent_knowledge_of_applicant(self):
        tools = []
        for tool_name, tool_info in self.documents_info.items():
            embeddings = OpenAIEmbeddings()
            index = FAISS.load_local(tool_info['save_path'], embeddings)
            retriever = index.as_retriever()

            tool = create_retriever_tool(
                retriever,
                tool_name,
                tool_info['description']
            )

            tools.append(tool)

        llm = ChatOpenAI(temperature=0.1)

        agent_executor = create_conversational_retrieval_agent(llm, tools, verbose=False)
        result = agent_executor({"input": "Tell me about Sean Bearden"})
        output = result["output"]
        self.assertTrue("Bearden" in output)
        self.assertTrue("Physics" in output)