# AI Healthcare System

## Technologes
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Amazon AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-<COLOR_CODE>?style=for-the-badge&logoColor=white)
![Langchain](https://img.shields.io/badge/Langchain-<COLOR_CODE>?style=for-the-badge&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=Snowflake&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?style=for-the-badge&logo=ApacheAirflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white)

## Demo
https://youtu.be/_N4aIHl-ldM

## CodeLab 
https://codelabs-preview.appspot.com/?file_id=1SRj1Bw5Mslf2abbsyFWPD23EjKr5ABgIgDURMa7c284#1
## Airflow
http://35.227.61.146:8080/home
## Streamlit
http://34.73.27.240:8501/

## Overview
The AI-Enhanced Healthcare Response System provides a user-friendly platform for symptom assessment and medication guidance. Integrated with CVS, it offers personalized health insights, streamlining access to treatments. The system aims to improve healthcare accessibility, early disease detection, and patient empowerment through efficient data management and resource optimization.

## Problem Statement
Current symptom assessment methods are inefficient, leading to unreliable self-diagnosis. Manual symptom analysis in healthcare is time-consuming, causing delays in diagnosis and treatment. Data management issues hinder healthcare efficiency and patient care. The project aims to address these challenges by automating symptom analysis, improving access to healthcare, and enhancing patient experience.

## Technology stack
- Apache Airflow: Workflow management and data processing.
- Pinecone Vector Databases: Efficient handling and retrieval of vectorized data.
- Google Cloud Platform (GCP): Hosting and cloud infrastructure.
- Pandas: Data manipulation and analysis.
- Jupyter Notebook: Data preprocessing, exploration and initial analysis.
- OpenAI: AI models for generating intelligent recommendations and embeddings.
- Streamlit: Interactive web application for patients.
- Snowflake: Secure and robust data storage,data handling.

## Project Description
Our system comprises these interconnected modules:

**Data Processing with Apache Airflow:**
- Manages and orchestrates data workflows.
- Processes diverse medical data sources for real-time insights.

**Pinecone and OpenAI for Personalized Recommendations:**
- Leverages Pinecone's vector database for efficient data retrieval and OpenAI's capabilities for intelligent data processing.
- Provides personalized medicine lists, CVS Store locations.
  
**Snowflake for Data Analysis and Storage:**
- Extracts the data from Amazon S3.
- Performed Data cleaning, formatting and modelling. Interacts with FastAPI.

**Streamlit-Based Portal:**
- A user-friendly interface for medical professionals to access patient information, input symptoms, and receive AI-driven diagnostic and treatment suggestions.

## Architecture Diagram
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team1/FinalProject/blob/main/Architecture%20Diagram.png)

## Dag1  Architecture Diagram

![image](https://github.com/BigDataIA-Spring2024-Sec1-Team1/FinalProject/blob/main/architecture_diagram.png)

## Dag2  Architecture Diagram

![image](https://github.com/BigDataIA-Spring2024-Sec1-Team1/FinalProject/blob/main/dag2.png)

## Dag3 and 4  Architecture Diagram

![image](https://github.com/BigDataIA-Spring2024-Sec1-Team1/FinalProject/blob/main/architecture_diagram1.png)

# How to use this repository

```plaintext
.
├── .gitignore
├── LICENSE
├── README.md
├── .github/workflows
   ├── superlinter.yml
├── airflow
│   ├── Dockerfile
│   ├── dags
│   │   ├── dag1.py
│   │   ├── dag2.py
│   │   └── dag3.py
│   │   ├── dag4.py
│   │   └── test.py
│   ├── logs
│   │   └── scheduler
│   │       └── latest
│   ├── requirements.txt
│   ├── Pipfile
│   ├── docker-compose.yaml
├── Streamlit
│   │   ├── final.py
│   │   ├── Pipfile
│   │   └── Pipfile.lock
│   │   ├── audio.mp3


```

## How to run the Application

- Download the code from github: https://github.com/BigDataIA-Spring2024-Sec1-Team1/FinalProject
- Run the Airflow from the above github repository or in your local
- Configure Snowflake in your local following the instructions from here
- Navigate to the following file and run it.
cd Snowflake 1.database.sql
- Initiate CI/CD in your github repository. By the end of CI/CD you should be able to see the Database configured with required datasets and connections.
- Run the Streamlit App after configuring the secrets. Or directly here. Streamlit.



## Instructions to run streamlit and Airflow locally

Download the streamlit folder and run the following commands

```plaintext
pipenv shell

pipenv install

streamlit run final.py

```

Download the Airflow folder and run the following commands

```plaintext
docker compose up --build
```



# References



Pinecone: Developed by OpenAI, Pinecone is an open-source Python library designed to leverage the functionalities of the GPT (Generative Pre-trained Transformer) models. It provides a user-friendly interface for fine-tuning, generating text, and conducting various natural language processing tasks with GPT models. Pinecone is equipped with features for text generation, completion, summarization, and more, making it a valuable tool for those engaged in natural language understanding and generation.

OpenAI GPT(https://openai.com/gpt): OpenAI's GPT (Generative Pre-trained Transformer) is a leading-edge natural language processing model known for its use of transformer architecture. Pre-trained on extensive text datasets, it excels at generating and interpreting text with a human-like quality. GPT models handle a broad array of language tasks such as text generation, completion, summarization, translation, and more, positioning them as essential tools in fields ranging from healthcare to entertainment.

Snowflake(https://www.snowflake.com/): Snowflake is a cloud-based data warehousing service that supports the storage, management, and analysis of large amounts of structured and semi-structured data. It is known for its scalability, flexibility, and high performance, which enable complex analytics and data insight extraction. The platform's architecture decouples storage and compute functions, allowing for independent scaling and optimizing costs. Snowflake enhances data analytics workflows with its SQL support and seamless integration with prevalent BI tools, enabling effective data-driven decision-making.


# Contributions
WE ATTEST THAT WE HAVEN'T USED ANY OTHER STUDENTS' WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

| Contributor | Contributions            | Percentage |
|-------------|--------------------------|------------|
| Dev Mithunisvar Premraj       | Airflow Orchestration, LLM |33.33%|
| Aneesh Koka        | Streamlit, LLM,Deployment | 33.33% |
| Rishabh Shah         | Streamlit, LLM, Snowflake, WhisperAI| 33.33% |







