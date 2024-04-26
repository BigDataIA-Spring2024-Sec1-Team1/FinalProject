from datetime import datetime, timedelta
from airflow import DAG
from dotenv import load_dotenv
from airflow.operators.python import PythonOperator
import pandas as pd
from io import BytesIO
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import numpy as np
import os
import requests
import io
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import requests
import numpy as np
import sys
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import os
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import OpenAIEmbeddings
import openai
from typing import Any, List
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
import pinecone
from pinecone import Pinecone, ServerlessSpec
import boto3
import re
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
import pinecone
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import numpy as np
from airflow.hooks.base_hook import BaseHook
from sqlalchemy.exc import SQLAlchemyError
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")



default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 29),
    'retries': 1,
}

dag = DAG('ingest_to_pinecone1_data_dag',
          default_args=default_args,
          description='A DAG to convert csv to daaframe',
          schedule_interval=None)

def process_recent_csv_from_s3(bucket_name, aws_conn_id='aws_default', **kwargs):
    s3_hook = S3Hook(aws_conn_id=aws_conn_id)
    s3_client = s3_hook.get_conn()
    objects = s3_client.list_objects_v2(Bucket=bucket_name)
    csv_files = [obj for obj in objects.get('Contents', []) if obj['Key'].endswith('.csv')]
    csv_files.sort(key=lambda x: x['LastModified'], reverse=True)

    if not csv_files:
        raise ValueError("No CSV files found in the bucket.")

    most_recent_csv = csv_files[0]['Key']
    obj = s3_hook.get_key(most_recent_csv, bucket_name=bucket_name)
    obj_content = obj.get()['Body'].read()
    dataframe = pd.read_csv(io.BytesIO(obj_content))

    # Serialize DataFrame to CSV and push as a string
    csv_data = dataframe.to_csv(index=False)
    return csv_data


def drop_nan_values(task_instance, **kwargs):
    csv_data = task_instance.xcom_pull(task_ids='process_recent_csv_from_s3_task')
    dataframe = pd.read_csv(io.StringIO(csv_data))
    # Drop NaN values
    clean_dataframe = dataframe.dropna()
    # Convert DataFrame to CSV string
    clean_csv_data = clean_dataframe.to_csv(index=False)
    return clean_csv_data

def print_first_five_rows(task_instance, **kwargs):
    ti = kwargs['ti']
    clean_csv_data = task_instance.xcom_pull(task_ids='data_structuring_task')
    dataframe = pd.read_csv(io.StringIO(clean_csv_data))
    print("First five rows of the cleaned DataFrame:")
    dataframe.reset_index(inplace=True)
    dataframe.rename(columns={'index': 'id'}, inplace=True)
    dataframe.loc[:, 'id'] += 1
    print(dataframe.head())
    initialize_pinecone()
    cc_pinecone1(dataframe)

def initialize_pinecone():
    try:
        # Load Pinecone configuration from environment variables
        api_key=os.getenv("PINECONE_API_KEY")
        environment="us-east1-gcp"
        if not api_key or not environment:
            print("Pinecone API key or environment is not set in environment variables.")
            sys.exit(1)
        
        # Initialize Pinecone
        pc = Pinecone(api_key=api_key, environment=environment)
        return pc
    except Exception as e:
        print(f"Failed to initialize Pinecone: {e}")
        sys.exit(1)


def cc_pinecone1(dataframe):
    df = dataframe
    Drug_Name = df['Drug_Name'].tolist()
    Symptoms = df['Symptoms'].tolist()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    
    api_key=os.getenv("PINECONE_API_KEY")
    environment="us-east1-gcp"

    pc = Pinecone(api_key=api_key, environment=environment)
    

    index_name = "drugsymptom"
# Create the vector store for the questions
    docsearch = PineconeVectorStore.from_texts(
        Drug_Name,
        embeddings,
        index_name=index_name,
        namespace="drug",
        metadatas=[{"id": i} for i in range(len(Drug_Name))]
    )

    docsearch = PineconeVectorStore.from_texts(
        Symptoms,
        embeddings,
        index_name=index_name,
        namespace="symptom",
        metadatas=[{"id": i} for i in range(len(Symptoms))]
    )

     



with dag:
    process_csv = PythonOperator(
        task_id='process_recent_csv_from_s3_task',
        python_callable=process_recent_csv_from_s3,
        op_kwargs={'bucket_name': 'finalprojecthealthcare'},
    )

    clean_csv = PythonOperator(
    task_id='data_structuring_task',
    python_callable=drop_nan_values,
    provide_context=True
)
    
    print_first_five_task = PythonOperator(
            task_id='pinecone_ingestion_task',
            python_callable=print_first_five_rows,
            provide_context=True
        )
    
     


    process_csv >> clean_csv >> print_first_five_task 
