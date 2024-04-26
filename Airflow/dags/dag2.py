from datetime import datetime, timedelta
from airflow import DAG, task
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
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import io
import re


def dataprocessing(df):
    dataframe = df

    # Check and drop rows with NaN values in specific columns if NaN values exist
    if dataframe.isnull().values.any():
        dataframe = dataframe.dropna(subset=['Drug_Name', 'Symptoms', 'Warning', 'Dosage'])

    # Remove special characters from specific columns
    def clean_text(text):
        # Regular expression to remove all non-alphanumeric characters except spaces
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)

    for column in ['Drug_Name', 'Symptoms', 'Warning', 'Dosage']:
        dataframe[column] = dataframe[column].apply(clean_text)

    return dataframe



openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 3),
    'retries': 1,
}

aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

session = boto3.Session(
    aws_access_key_id= aws_access_key_id, #kept blank due to privacy issue,
    aws_secret_access_key=aws_secret_access_key,#kept blank due to privacy issue,
)

s3 = session.client('s3')


dag = DAG('process_csv_data_dag',
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




def datacleaning(task_instance, **kwargs):
    csv_data = task_instance.xcom_pull(task_ids='process_recent_csv_from_s3_task')
    dataframe = pd.read_csv(io.StringIO(csv_data))

    # Check and drop rows with NaN values in specific columns if NaN values exist
    if dataframe.isnull().values.any():
        dataframe = dataframe.dropna(subset=['Drug_Name', 'Symptoms', 'Warning', 'Dosage'])

    # Remove special characters from specific columns
    def clean_text(text):
        # Regular expression to remove all non-alphanumeric characters except spaces
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)

    for column in ['Drug_Name', 'Symptoms', 'Warning', 'Dosage']:
        dataframe[column] = dataframe[column].apply(clean_text)

    dataframe = dataprocessing(dataframe)
    # Convert DataFrame to CSV string
    dataframe = dataframe.dropna()
    clean_csv_data = dataframe.to_csv(index=False)
    return clean_csv_data


def openaiextraction(task_instance, **kwargs):
    ti = kwargs['ti']
    clean_csv_data = task_instance.xcom_pull(task_ids='datacleaning_task')
    # Ensure the data is read correctly into a DataFrame
    dataframe = pd.read_csv(io.StringIO(clean_csv_data))
    


    summary_template = """
        For the given {symptoms} exctract the symptoms and the organ from the text. For the given {warning} extract the warning about the drugs. Give the symptoms starting with'$'
        and warning with '&'. If No Symptoms or warning are found return Not-found for the value.
        """

    summary_prompt_template = PromptTemplate(
            input_variables=["information"], template=summary_template
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)


    result_df = pd.DataFrame(columns=['Drug_Name', 'Symptoms', 'Warning', 'Dosage'])

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    for index, row in dataframe.iterrows():
        # Extracting symptoms and warning data
        symptoms_data = row['Symptoms']
        warning_data = row['Warning']

        # Invoking the LLM chain with the extracted data
        res = chain.invoke(input={"symptoms": symptoms_data, "warning": warning_data})

        # Printing the result for each row
        print(f"Row {index + 1}: {res.get('text', 'No content available.')}")
        response_text = res.get('text', 'No content available.')

        if '&' in response_text:
            parts = response_text.split('&')
            symptoms_part = parts[0].strip('$').strip()
            warning_part = parts[1].strip()
        else:
            symptoms_part = response_text.strip('$').strip()
            warning_part = "No warning data available."

        # Create a DataFrame for the new row
        new_row = pd.DataFrame({
            'Drug_Name': [row['Drug_Name']],  
            'Symptoms': [symptoms_part],
            'Warning': [warning_part],
            'Dosage': [row['Dosage']]
        })

        # Append the new row to the result DataFrame
        result_df = pd.concat([result_df, new_row], ignore_index=True)

    print(result_df.head())
    result_df = result_df[~result_df['Symptoms'].isin(['Symptoms Notfound', 'Notfound','Symptoms: Not-found'])]
    result_df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

    result_df = result_df.dropna()

    filename = "Mark1.csv"
    result_df = dataprocessing(result_df)
    result_df.to_csv(filename, index=False)  
    with open(filename, "rb") as f:
        s3.upload_fileobj(f, S3_BUCKET_NAME, filename)

    ti.xcom_push(key='processed_data', value=result_df.to_json(orient='split'))

    return result_df


def upload_to_database(**kwargs):
    ti = kwargs['ti']
    df_json = ti.xcom_pull(key='processed_data', task_ids='openaiextraction_task')
    df = pd.read_json(df_json, orient='split')
    df.columns = [c.upper() for c in df.columns]
    df = df.dropna() 

    # Constants for Snowflake
    DB_NAME = os.getenv("DB_NAME")
    WAREHOUSE = os.getenv("WAREHOUSE")
    TABLECONTENT = os.getenv("TABLECONTENT")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    ACCOUNT = os.getenv("ACCOUNT")




    # Configure connection URL for Snowflake
    connection_url = URL.create(
        "snowflake",
        username=USERNAME,
        password=PASSWORD,
        host=ACCOUNT,
        database=DB_NAME,
        query={
            'warehouse': WAREHOUSE,
            'role': 'ACCOUNTADMIN',  # Adjust role as necessary
        }
    )

    engine = create_engine(connection_url)

    try:
        with engine.connect() as conn:
            # Setup database and warehouse
            conn.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            conn.execute(f"CREATE WAREHOUSE IF NOT EXISTS {WAREHOUSE} WITH WAREHOUSE_SIZE = 'X-SMALL' AUTO_SUSPEND = 180 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE")
            conn.execute(f"USE WAREHOUSE {WAREHOUSE}")
            conn.execute(f"USE DATABASE {DB_NAME}")

            conn.execute(f"DROP TABLE IF EXISTS {TABLECONTENT};")


            # Setup tables
            conn.execute(f"""CREATE TABLE IF NOT EXISTS {TABLECONTENT} (
                Drug_Name TEXT,
                Symptoms TEXT,
                Warning TEXT,
                Dosage TEXT
            );""")
          
                    

            
            df.to_sql(TABLECONTENT, con=conn, if_exists='append', index=False, schema='PUBLIC')

            print('Data upload successful.')

    except Exception as error:
        print(f"An error occurred: {error}")

    finally:
        engine.dispose()

    




trigger = TriggerDagRunOperator(
    task_id = 'trigger_target_dag',
    trigger_dag_id = 'ingest_to_pinecone1_data_dag',
    wait_for_completion = True,
    execution_date = '{{ ds }}'


)




with dag:
    process_csv = PythonOperator(
        task_id='process_recent_csv_from_s3_task',
        python_callable=process_recent_csv_from_s3,
        op_kwargs={'bucket_name': 'finalprojecthealthcare'},
    )

    clean_csv = PythonOperator(
    task_id='datacleaning_task',
    python_callable=datacleaning,
    provide_context=True
)
    
    print_first_five_task = PythonOperator(
            task_id='openaiextraction_task',
            python_callable=openaiextraction,
            provide_context=True
        )
    
    upload_db = PythonOperator(
        task_id='upload_to_database_task',
        python_callable=upload_to_database,
        provide_context=True
    )    

    


    process_csv >> clean_csv >> print_first_five_task >> upload_db 
 
