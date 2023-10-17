# resume-chatbot
A chatbot for recruiters to query information about a job applicant.

## Usage
1. Upload applicant text files into [res/data](./res/data) directories. Each directory becomes a tool. Add or remove directories if 
   desired. Confirm the directories are described in [documents_info.json](./res/data/documents_info.json). 
2. Run [create_vector_store.py](./create_vector_store.py) to create index databases with FAISS.
3. Set up heroku deploy. Must have gunicorn in [requirements.txt](./requirements.txt).

## Data
Create vector stores for:
* Resume
* CV
* Website
* GitHub
* Thesis


## References
* A modification of a Dash Gallery app: https://github.com/dkedar7/embedchain-fastdash
* Agent with retrieval tool: https://python.langchain.com/docs/use_cases/question_answering/conversational_retrieval_agents