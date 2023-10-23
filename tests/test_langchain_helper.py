from langchain.document_loaders import TextLoader
import unittest
from unittest.mock import MagicMock, patch
from tools.langchain_helper import create_vector_stores


class TestCreateVectorStores(unittest.TestCase):

    @patch('tools.langchain_helper.DirectoryLoader')
    @patch('tools.langchain_helper.CharacterTextSplitter')
    @patch('tools.langchain_helper.OpenAIEmbeddings')
    @patch('tools.langchain_helper.FAISS')
    @patch('tools.langchain_helper.create_nested_directory')
    def test_create_vector_stores_text_only(
            self,
            mock_create_nested_directory,
            mock_faiss,
            mock_embeddings,
            mock_text_splitter,
            mock_directory_loader
    ):
        documents_info = {
            'tool1': {
                'directory_path': 'path/to/documents',
                'save_path': 'path/to/save'
            }
        }

        create_vector_stores(documents_info, text_only=True)

        mock_directory_loader.assert_called_once_with(
            'path/to/documents', glob="**/*.txt", loader_cls=TextLoader
        )
        mock_text_splitter.assert_called_once_with(chunk_size=1000, chunk_overlap=0)
        mock_create_nested_directory.assert_called_once_with('path/to/save')


if __name__ == '__main__':
    unittest.main()
