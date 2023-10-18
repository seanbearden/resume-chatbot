# resume-chatbot
A chatbot for recruiters to query information about a job applicant.
See an example [here](https://bearden-resume-chatbot-2d3e7f033a89.herokuapp.com)

## Usage
1. Upload applicant text files into [res/data](./res/data) directories. Each directory becomes a tool. Add or remove directories if 
   desired. Confirm the directories are described in [documents_info.json](./res/data/documents_info.json). 
2. Run [create_vector_store.py](./create_vector_store.py) to create index databases with FAISS.
3. Set up heroku deploy. Must have gunicorn in [requirements.txt](./requirements.txt). From the terminal use the 
   Heroku CLI to deploy following along with [this documentation](https://devcenter.heroku.com/articles/creating-apps)

## Data
Create vector stores for:
* Resume
* CV
* Website
* GitHub
* Thesis

## Custom Domain
```(venv) resume-chatbot$ heroku domains:add www.bearden-resume-bot.com
Configure your app's DNS provider to point to the DNS Target 
mechanistic-toucan-8v8puv00b8px1luvx3unvi5c.herokudns.com.
    For help, see https://devcenter.heroku.com/articles/custom-domains

The domain www.bearden-resume-bot.com has been enqueued for addition
Run heroku domains:wait 'www.bearden-resume-bot.com' to wait for completion
Adding www.bearden-resume-bot.com to ⬢ bearden-resume-chatbot... done
```

## References
* A modification of a Dash Gallery app: https://github.com/dkedar7/embedchain-fastdash
* Agent with retrieval tool: https://python.langchain.com/docs/use_cases/question_answering/conversational_retrieval_agents