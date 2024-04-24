# FinalProject
Big Data Final Project


## CodeLab 
https://codelabs-preview.appspot.com/?file_id=1CtC72t9EJxhyDA-04CaVzQOXvmUvcP1naWeVDfIpUyA#8
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
- FastAPI: Backend service management.
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

**FastAPI for Backend Services:**
- Handles requests from the Streamlit frontend, interacting with Pinecone and OpenAI.
- Integrates with a PostgreSQL database for robust data management.

## Architecture Diagram
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team1/FinalProject/assets/144849239/6d023bda-1fd5-4314-a64e-5032ae2e58cd)

# How to use this repository

Airflow  
├── Dockerfile  
├── dags  
│   └── dag1  
│       └── main.py  
├── docker-compose.yaml  
├── logs  
│   └── scheduler  
│       └── latest -> /opt/airflow/logs/scheduler/2024-04-24 
└── requirements.txt  
README.md  
Snowflake  
├── database.sql  
├── 1.load_data.py  
├── 2.Normalization.py  
└── convert_xlsx_to_csv.py  
Streamlit  
├── Home.py  
├── .csv  
├── images  
│   └── black.jpeg  
└── pages  
    ├── About.py  
    └── patient.py  
├── requirements.txt  
└── test.py  
fastapi  
├── Profile  
│   └── main.py  
└── requirements.txt  
└── runtime.txt

## How to run the Application

- Download the code from github: https://github.com/BigDataIA-Spring2024-Sec1-Team1/FinalProject
- Run the Airflow from the above github repository or in your local
- Configure Snowflake in your local following the instructions from here
- Navigate to the following file and run it.
cd Snowflake 1.database.sql
- Initiate CI/CD in your github repository. By the end of CI/CD you should be able to see the Database configured with required datasets and connections.
- Create an RDS with preferably PostgreSQL database.
- Run the Streamlit App after configuring the secrets. Or directly here. Streamlit.











