# Ask The Resume Chatbot

Engage recruiters and hiring managers effortlessly with a chatbot that personifies your professional journey. The Professional Resume Chatbot is designed to facilitate an interactive exploration of a job seeker's credentials, encompassing resumes, CVs, publications, projects, and more. Tailor the chatbot's responses through a predefined Q&A segment to ensure it aligns with your narrative. Hosted on Heroku, this chatbot delivers a personalized user experience by engaging with session histories. All interactions are securely logged in a DynamoDB table, set up through AWS Serverless Application Model (SAM).

Explore a live demonstration at [bearden-resume-chatbot.com](https://www.bearden-resume-chatbot.com).

## Getting Started

### Preparation
1. Populate the [res/data](./res/data) directories with the applicant's files, preferably text files to optimize costs. (A sample PDF is included). Each directory here acts as a distinct tool. Add or remove directories as required, ensuring they are duly listed in [documents_info.json](./res/data/documents_info.json) to aid the chatbot in tool selection.

### Indexing
2. Execute [create_vector_store.py](./create_vector_store.py) to establish index databases via FAISS.

### Deployment
3. Prepare for Heroku deployment ensuring `gunicorn` is listed in [requirements.txt](./requirements.txt). Utilize the Heroku CLI for deployment as outlined in [Heroku's Documentation](https://devcenter.heroku.com/articles/creating-apps).
4. Configure key-value pairs on Heroku.
5. Run the following commands to build and deploy the application:
    ```bash
    sam build
    sam deploy --guided
    git add .
    git commit -m "initial commit"
    git push heroku main
    ```

## Data Vector Stores
- Resume
- CV
- Website
- Projects
- Publications

## Custom Domain (Optional)
For a personalized domain, consider procuring or transferring a domain via Cloudflare. Follow the guidelines provided [here](https://developers.cloudflare.com/support/third-party-software/others/configure-cloudflare-and-heroku-over-https/) to ensure a smooth setup.

## Acknowledgments
- Adapted from a Dash Gallery application: [Embedchain-Fastdash](https://github.com/dkedar7/embedchain-fastdash)
- Conversational retrieval agent utility: [Langchain Documentation](https://python.langchain.com/docs/use_cases/question_answering/conversational_retrieval_agents)
- Chat vector database enhancement: [Langchain Documentation](https://python.langchain.com/docs/use_cases/question_answering/chat_vector_db)