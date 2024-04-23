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
- Streamlit: Interactive web application for doctors and patients.
- FastAPI: Backend service management.
- Snowflake: Secure and robust data storage,data handling.

## Project Description
Our system comprises these interconnected modules:

### Data Processing with Apache Airflow:
- Manages and orchestrates data workflows.
- Processes diverse medical data sources for real-time insights.

### Pinecone and OpenAI for Personalized Recommendations:
- Leverages Pinecone's vector database for efficient data retrieval and OpenAI's capabilities for intelligent data processing.
- Provides personalized medicine lists, doctor suggestions, and hospital recommendations.
  
### Snowflake for Data Analysis and Storage:
- Extracts the data from Amazon S3.
- Performed Data cleaning, formatting and modelling. Interacts with FastAPI.

### Streamlit-Based Doctor's Portal:
- A user-friendly interface for medical professionals to access patient information, input symptoms, and receive AI-driven diagnostic and treatment suggestions.

### FastAPI for Backend Services:
- Handles requests from the Streamlit frontend, interacting with Pinecone and OpenAI.
- Integrates with a PostgreSQL database for robust data management.


