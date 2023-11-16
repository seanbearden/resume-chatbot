# Ask The Resume Chatbot

## Overview
Engage recruiters and hiring managers effortlessly with a chatbot that personifies your professional journey. The Professional Resume Chatbot is designed for interactive exploration of a job seeker's credentials, including resumes, CVs, publications, and projects. Hosted on Heroku and utilizing AWS Serverless Application Model (SAM) for secure logging, this chatbot offers a personalized experience through session histories.

**Live Demo:** [bearden-resume-chatbot.com](https://www.bearden-resume-chatbot.com)

## Table of Contents
- [Getting Started](#getting-started)
- [Data Vector Stores](#data-vector-stores)
- [Custom Domain](#custom-domain-optional)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [FAQs/Troubleshooting](#faqs/troubleshooting)
- [Acknowledgments](#acknowledgments)
- [License](#license)
- [Contact](#contact)

## Getting Started
### Preparation
1. Populate `res/data` directories with the applicant's files (text files preferred for cost optimization).
2. Update `documents_info.json` for chatbot tool selection.

### Indexing
- Run [create_vector_store.py](./create_vector_store.py) to establish index databases via FAISS.

### Deployment
- Prepare Heroku deployment (ensure `gunicorn` in `requirements.txt`).
- Configure key-value pairs on Heroku.
- Build and deploy using SAM, must specify Docker context `DOCKER_ENDPOINT`. Follow [these](https://github.
   com/aws/aws-sam-cli/issues/4329#issuecomment-1732670902) instructions to determine location of host.
    ```bash
    DOCKER_HOST=DOCKER_ENDPOINT sam build --use-container -t template.yaml
    DOCKER_HOST=DOCKER_ENDPOINT sam deploy --guided

    ```
- Run the following commands to deploy on heroku:
    ```bash
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
For a personalized domain, set up via Cloudflare. [Cloudflare setup guide](https://developers.cloudflare.com).

## Usage Examples
(Include specific text examples or screenshots demonstrating chatbot interactions)

## Contributing
(Outline how others can contribute to the project)

## FAQs/Troubleshooting
(Address common issues or questions)

## Acknowledgments
- Adapted from a Dash Gallery application: [Embedchain-Fastdash](https://github.com/dkedar7/embedchain-fastdash)
- Conversational retrieval agent utility: [Langchain Documentation](https://python.langchain.com/docs/use_cases/question_answering/conversational_retrieval_agents)
- Chat vector database enhancement: [Langchain Documentation](https://python.langchain.com/docs/use_cases/question_answering/chat_vector_db)

## License
(Mention the project's license here)

## Contact
(Provide contact information for queries or contributions)
