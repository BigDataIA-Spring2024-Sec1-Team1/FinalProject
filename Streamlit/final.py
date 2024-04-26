import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
from dotenv import load_dotenv
import os
import requests
import pandas as pd
import streamlit as st
from langchain.chains import LLMChain
#from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import streamlit as st
#from fastapi import FastAPI
import requests
import numpy as np
#app=FastAPI()
import sys
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import os
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import OpenAIEmbeddings
import random
import openai
from pinecone import PodSpec
from typing import Any, List
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
import pinecone
from pinecone import Pinecone, ServerlessSpec
import boto3
from io import StringIO
import re
import string
import pinecone
from langchain import VectorDBQA, OpenAI
import logging
import sys
from streamlit_chat import message
import snowflake.connector 
from datetime import datetime
from snowflake.connector.pandas_tools import write_pandas
import streamlit as st
import pandas as pd
import snowflake.connector
from fpdf import FPDF
from io import BytesIO
from tabulate import tabulate
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_chat import message
import time
from wordcloud import WordCloud

# Set up the session state variables
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'login'
if 'username' not in st.session_state:
    st.session_state['username'] = ''



def plot():
    USERNAME = 'DEV'
    PASSWORD = 'Dev12345'
    ACCOUNT = 'phdsaxs-kib61200'
    DB_NAME = 'HealthResponseSystem'
    WAREHOUSE = 'COMPUTE_WH'
    TABLECONTENT= 'MEDICATIONHISTORY'

    # Configure connection URL for Snowflake
    conn= snowflake.connector.connect(
         user=USERNAME,
                                password=PASSWORD,
                                account=ACCOUNT,
                                warehouse=WAREHOUSE,
                                database=DB_NAME,
                                schema='PUBLIC',
                                role='ACCOUNTADMIN'
                            )

    cur=conn.cursor()
    sql_query = "SELECT * FROM MEDICATIONHISTORY"
    cur.execute(sql_query)
    data_fetch=cur.fetchall()
    df=pd.DataFrame(data_fetch, columns=['Date','Drug_Name','Output','Symptoms','USERNAME'])

    # Generate text for the word cloud from the DataFrame column
    drug_name = ' '.join(df['Drug_Name'].astype(str))

    # Counting occurrences of each disease
    disease_counts = df['Drug_Name'].value_counts()

    # Create a Matplotlib figure and axis object
    fig, ax = plt.subplots()

    # Plotting the counts of repeated diseases
    disease_counts.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Drug Name Frequency Plot')
    ax.set_xlabel('DrugName')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45, ha='right')

    # Return the figure object
    return fig

def word_cloud():
    USERNAME = 'DEV'
    PASSWORD = 'Dev12345'
    ACCOUNT = 'phdsaxs-kib61200'
    DB_NAME = 'HealthResponseSystem'
    WAREHOUSE = 'COMPUTE_WH'
    TABLECONTENT= 'MEDICATIONHISTORY'

    # Configure connection URL for Snowflake
    conn= snowflake.connector.connect(
         user=USERNAME,
                                password=PASSWORD,
                                account=ACCOUNT,
                                warehouse=WAREHOUSE,
                                database=DB_NAME,
                                schema='PUBLIC',
                                role='ACCOUNTADMIN'
                            )

    cur=conn.cursor()
    sql_query = "SELECT * FROM MEDICATIONHISTORY"
    cur.execute(sql_query)
    data_fetch=cur.fetchall()
    df=pd.DataFrame(data_fetch, columns=['Date','Drug_Name','Output','Symptoms','Username'])

    # Generate text for the word cloud from the DataFrame column
    symptoms = ' '.join(df['Symptoms'].astype(str))
    
    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(symptoms)

    # Set up matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the size to fit your needs
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Hide the axes
    ax.set_title("Word Cloud for Symptoms")

    # Display the figure in Streamlit
    return fig





logging.basicConfig(level=logging.INFO)

api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)


def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        # Assuming 'Audio.transcribe' is the correct function based on API documentation
        transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file)
        return transcript['text']

def fetch_ai_response(input_text):
    messages = [{"role": "user", "content": input_text}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-1106", messages=messages)
    return response.choices[0].message.content

def initialize_pinecone():
    try:
        # Load Pinecone configuration from environment variables
        api_key = os.getenv("PINECONE_API_KEY")
        environment = os.getenv("PINECONE_ENVIRONMENT_REGION")
        if not api_key or not environment:
            logging.error("Pinecone API key or environment is not set in environment variables.")
            sys.exit(1)
        
        # Initialize Pinecone
        pc = Pinecone(api_key=api_key, environment=environment)
        return pc
    except Exception as e:
        logging.error(f"Failed to initialize Pinecone: {e}")
        sys.exit(1)



def is_valid_password(password):
    return (len(password) >= 8 and re.search("[A-Z]", password) and
            re.search("[a-z]", password) and re.search("[0-9]", password))

def is_valid_age(age):
    try:
        return 0 < int(age) <= 120
    except ValueError:
        return False

# Function to handle database operations
import logging
logging.basicConfig(level=logging.INFO)

def write_data_to_snowflake(df):
    # Constants for Snowflake connection
    USERNAME = 'DEV'
    PASSWORD = 'Dev12345'
    ACCOUNT = 'phdsaxs-kib61200'
    DB_NAME = 'HealthResponseSystem'
    WAREHOUSE = 'COMPUTE_WH'
    TABLECONTENT = 'USERDETAILS'
    
    conn = snowflake.connector.connect(
        user=USERNAME,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
        database=DB_NAME,
        schema='PUBLIC',
        role='ACCOUNTADMIN'
    )

    # Create or replace table if not exists (consider changing to "CREATE TABLE IF NOT EXISTS" for production)
    cur = conn.cursor()
    #cur.execute('INSERT INTO TABLE "USERDETAILS"("Username" VARCHAR, "Age" INT, "Gender" VARCHAR, "Email" VARCHAR, "Password" VARCHAR, "Address" VARCHAR, "Zipcode" VARCHAR, "MedicalHistory" VARCHAR)')
    #write_pandas(conn, df, TABLECONTENT)
    success, nchunks, nrows, _ = write_pandas(conn, df, TABLECONTENT)
    print(f"Successfully written: {success}, Number of chunks: {nchunks}, Number of rows: {nrows}")
    cur.close()
    conn.close()

# Streamlit registration page
def registration():
    st.title("Registration Page")
    username = st.text_input("Username")
    email = st.text_input("Email")
    age = st.text_input("Age")
    gender = st.selectbox('Gender', ('Male', 'Female'))
    address = st.text_input("Address")
    zipcode = st.text_input("Zipcode")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    history= st.text_input("Medical History")

    if st.button('✍️ Create Profile'):
        if not is_valid_age(age):
            st.error("Please enter a valid age.")
            return
        elif password != confirm_password:
            st.error("Passwords do not match. Please try again.")
            return
        elif not is_valid_password(password):
            st.error("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.")
            return

        user_data = {
            'USERNAME': [username],
            'Age': [age],
            'Gender': [gender],
            'Email': [email],
            'Password': [password],
            'Address': [address],
            'Zipcode': [zipcode] ,
            'MedicalHistory': [history] 
        }
        
        df = pd.DataFrame(user_data)
        write_data_to_snowflake(df)  # Call the function to write data to Snowflake
        st.session_state.authenticated = False

        st.session_state.current_page = 'login'
        



def testrun_drug(query, i):
                            i=i
                            query=query
                            pc = Pinecone(
                            api_key=os.getenv("PINECONE_API_KEY"),
                            environment="us-east1-gcp"
                            )
                            index_name = 'drugsymptom'
                            index = pc.Index(index_name)
                            embeddings = OpenAIEmbeddings()
                            set_b_only_questions_vectors = embeddings.embed_query(query)
                            symptomsarray=[]
                            symptomsarray.append(index.query(vector=set_b_only_questions_vectors, top_k=1, namespace='symptom', include_metadata=True, include_values=True))
                            answer_ids = []
                            for question in symptomsarray[0].matches: 
                                q =  question
                            answer_ids.append(index.query(vector=q.values, top_k=i, namespace='drug', include_metadata=True))
                            drugname= answer_ids[0].matches[i-1].metadata['text'] 
                            #st.write("The Prescribed drug: ",answer_ids[i-1].matches[i-1].metadata['text'])
                            # Constants for Snowflake
                            USERNAME = 'DEV'
                            PASSWORD = 'Dev12345'
                            ACCOUNT = 'phdsaxs-kib61200'
                            DB_NAME = 'HealthResponseSystem'
                            WAREHOUSE = 'COMPUTE_WH'
                            TABLECONTENT= 'Medication'

                            # Configure connection URL for Snowflake
                            conn= snowflake.connector.connect(
                                user=USERNAME,
                                password=PASSWORD,
                                account=ACCOUNT,
                                warehouse=WAREHOUSE,
                                database=DB_NAME,
                                schema='PUBLIC',
                                role='ACCOUNTADMIN'
                            )

                            cur=conn.cursor()
                            sql_query = """SELECT DISTINCT DOSAGE FROM "Medication" WHERE DRUG_NAME = %s"""
                            cur.execute(sql_query, (drugname))
                            data_fetch=cur.fetchall()
                            df=pd.DataFrame(data_fetch, columns=['Dosage'])
                            dosage= df['Dosage'][0]
                            summary_template = """
                       You are a doctor generating a prescription for the patient on when and how to take the drug: {drugname} with the corresponding dosage: {dosage}. Make {drugname} as heading and {dosage} below. 
                        """
                            summary_prompt_template = PromptTemplate(
                            input_variables=["drugname", "dosage"], template=summary_template
                        )
                            openai_api_key= os.environ['OPENAI_API_KEY']
                            llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)



                            chain = LLMChain(llm=llm, prompt=summary_prompt_template)

                            result = chain.invoke(input={"drugname": drugname, "dosage": dosage})
                            write = result['text']
                            st.session_state['username']
                            user_data = {
                        'Date': [datetime.now().strftime('%Y-%m-%d')],
                        'Drug_Name': [drugname],
                        'Output': [result['text']],
                        'Symptoms': [query],
                        'USERNAME': [st.session_state['username']]
                    }
                            
                    
                            df = pd.DataFrame(user_data)
                            
                            # Constants for Snowflake
                            USERNAME = 'DEV'
                            PASSWORD = 'Dev12345'
                            ACCOUNT = 'phdsaxs-kib61200'
                            DB_NAME = 'HealthResponseSystem'
                            WAREHOUSE = 'COMPUTE_WH'
                            TABLECONTENT= 'MEDICATIONHISTORY'

                            # Configure connection URL for Snowflake
                            conn= snowflake.connector.connect(
                                user=USERNAME,
                                password=PASSWORD,
                                account=ACCOUNT,
                                warehouse=WAREHOUSE,
                                database=DB_NAME,
                                schema='PUBLIC',
                                role='ACCOUNTADMIN'
                            )

                            cur=conn.cursor()
                            success, nchunks, nrows, _ = write_pandas(conn, df, TABLECONTENT)
                            print(f"Successfully written: {success}, Number of chunks: {nchunks}, Number of rows: {nrows}")
                            cur.close()
                            conn.close()
                            return write


def testrun_drug_warn(query,j):
                        i=j
                        query=query
                        pc = Pinecone(
                        api_key=os.getenv("PINECONE_API_KEY"),
                        environment="us-east1-gcp"
                        )
                        index_name = 'drugsymptom'
                        index = pc.Index(index_name)
                        embeddings = OpenAIEmbeddings()
                        set_b_only_questions_vectors = embeddings.embed_query(query)
                        symptomsarray=[]
                        symptomsarray.append(index.query(vector=set_b_only_questions_vectors, top_k=1, namespace='symptom', include_metadata=True, include_values=True))
                        answer_ids = []
                        for question in symptomsarray[0].matches: 
                                q =  question
                        answer_ids.append(index.query(vector=q.values, top_k=i, namespace='drug', include_metadata=True))
                        drugname= answer_ids[0].matches[i-1].metadata['text'] 
                        USERNAME = 'DEV'
                        PASSWORD = 'Dev12345'
                        ACCOUNT = 'phdsaxs-kib61200'
                        DB_NAME = 'HealthResponseSystem'
                        WAREHOUSE = 'COMPUTE_WH'
                        TABLECONTENT= 'Medication'

                            # Configure connection URL for Snowflake
                        conn= snowflake.connector.connect(
                                user=USERNAME,
                                password=PASSWORD,
                                account=ACCOUNT,
                                warehouse=WAREHOUSE,
                                database=DB_NAME,
                                schema='PUBLIC',
                                role='ACCOUNTADMIN'
                            )

                        cur=conn.cursor()
                        sql_query = """SELECT DISTINCT DOSAGE FROM "Medication" WHERE DRUG_NAME = %s"""
                        cur.execute(sql_query, (drugname))
                        data_fetch=cur.fetchall()
                        df=pd.DataFrame(data_fetch, columns=['Dosage'])
                        dosage= df['Dosage'][0]
                        summary_template = """
                       You are a chatbot generating a prescription for the patient on when and how to take the drug: {drugname} with the corresponding dosage: {dosage}. Make {drugname} as heading and {dosage} below. Also add a warning note to visit a doctor before taking the drug given taht the users medical history aligns with the warnings of the drug and caution him about taking it.
                        """
                        summary_prompt_template = PromptTemplate(
                        input_variables=["drugname", "dosage"], template=summary_template
                        )
                        openai_api_key= os.environ['OPENAI_API_KEY']
                        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)



                        chain = LLMChain(llm=llm, prompt=summary_prompt_template)

                        result = chain.invoke(input={"drugname": drugname, "dosage": dosage})
                        write = result['text']
                        return write


                           
                         


def testrun_warning(query, ii):
                        warning = ""
                        i=ii
                        query = query
                        pc = Pinecone(
                        api_key=os.getenv("PINECONE_API_KEY"),
                        environment="us-east1-gcp"
                        )
                        index_name = 'drugsymptom'
                        index = pc.Index(index_name)
                        embeddings = OpenAIEmbeddings()
                        set_b_only_questions_vectors = embeddings.embed_query(query)
                        symptomsarray=[]
                        symptomsarray.append(index.query(vector=set_b_only_questions_vectors, top_k=1, namespace='symptom', include_metadata=True, include_values=True))
                        answer_ids = []
                        for question in symptomsarray[0].matches:
                            q =  question
                        for i in range(i+1):
                            answer_ids.append(index.query(vector=q.values, top_k=i+1, namespace='drug', include_metadata=True))
                            drugname= answer_ids[i].matches[i].metadata['text'] 
                            # Constants for Snowflake
                            USERNAME = 'DEV'
                            PASSWORD = 'Dev12345'
                            ACCOUNT = 'phdsaxs-kib61200'
                            DB_NAME = 'HealthResponseSystem'
                            WAREHOUSE = 'COMPUTE_WH'
                            TABLECONTENT= 'Medication'

                            # Configure connection URL for Snowflake
                            conn= snowflake.connector.connect(
                                user=USERNAME,
                                password=PASSWORD,
                                account=ACCOUNT,
                                warehouse=WAREHOUSE,
                                database=DB_NAME,
                                schema='PUBLIC',
                                role='ACCOUNTADMIN'
                            )

                            cur=conn.cursor()
                            sql_query = """SELECT DISTINCT Warning FROM "Medication" WHERE DRUG_NAME = %s"""
                            cur.execute(sql_query, (drugname))
                            data_fetch=cur.fetchall()
                            df=pd.DataFrame(data_fetch)
                            warning = df.iloc[0]

                        return warning




def run_llm(query: str) -> str:
        information = query
        summary_template = """
        Is the following text related to healthcare? \"{information}\" Provide a simple yes or no answer.
        """

        summary_prompt_template = PromptTemplate(
            input_variables=["information"], template=summary_template
        )

        openai_api_key= os.environ['OPENAI_API_KEY']
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)



        chain = LLMChain(llm=llm, prompt=summary_prompt_template)

        res = chain.invoke(input={"information": information})
            # Update the session state variable instead of a local variable
        if res['text'] == 'No':
            write = "The text is not a symptom."
            return write
        else:
                summary_template = """
            extract the symptoms from {information} and just mention the symptoms. 
            """
                summary_prompt_template = PromptTemplate(
                input_variables=["information"], template=summary_template
            )

                openai_api_key= os.environ['OPENAI_API_KEY']
                llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)



                chain = LLMChain(llm=llm, prompt=summary_prompt_template)

                keywords = chain.invoke(input={"information": information})
                pc = Pinecone(
                api_key= os.getenv("PINECONE_API_KEY"),
                environment="us-east1-gcp"
                    )
                index_name= 'diseases'
                index = pc.Index(index_name)

                embeddings = OpenAIEmbeddings()
                set_b_only_questions_vectors = embeddings.embed_query(query)
                question_t3 = index.query(vector=set_b_only_questions_vectors, top_k=1, namespace='symptom', include_metadata=True)
                symptomsarray=[]
                symptomsarray.append(index.query(vector=set_b_only_questions_vectors, top_k=1, namespace='symptom', include_metadata=True, include_values=True))
                if symptomsarray[0].matches[0].score>0.9:
                        answer_ids = []
                        for question in symptomsarray[0].matches: 
                            answer_ids.append(index.query(vector=question.values, top_k=1, namespace='disease', include_metadata=True))
                        information = answer_ids[0].matches[0].metadata['text']
                        summary_template = """
                    Please mention that the symptoms entered by the user is smilar {information} disease and mention that you need to visit a doctor
                    """
                        summary_prompt_template = PromptTemplate(
                        input_variables=["information"], template=summary_template
                    )
                        openai_api_key= os.environ['OPENAI_API_KEY']
                        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)



                        chain = LLMChain(llm=llm, prompt=summary_prompt_template)

                        result = chain.invoke(input={"information": information})
                        write = result['text']
                        return write
                else:
                        USERNAME = 'DEV'
        PASSWORD = 'Dev12345'
        ACCOUNT = 'phdsaxs-kib61200'
        DB_NAME = 'HealthResponseSystem'
        WAREHOUSE = 'COMPUTE_WH'
        TABLECONTENT= 'USERDETAILS'

        # Configure connection URL for Snowflake
        conn= snowflake.connector.connect(
            user=USERNAME,
                                    password=PASSWORD,
                                    account=ACCOUNT,
                                    warehouse=WAREHOUSE,
                                    database=DB_NAME,
                                    schema='PUBLIC',
                                    role='ACCOUNTADMIN'
                                )

        cur=conn.cursor()
        user_name= st.session_state['username']
        sql_query = """SELECT * FROM "USERDETAILS" where USERNAME = %s"""
        cur.execute(sql_query,(user_name))
        data_fetch=cur.fetchall()
        df=pd.DataFrame(data_fetch,columns=['Username','Age','Gender','Email','Password','Address','Zipcode','MedicalHistory'])

        # Previous Data (Replace with your actual previous data retrieval logic)
        history=df['MedicalHistory'][0]
        i=1
        j=0
        while j!=3:
                    warning = testrun_warning(information,i)
                    summary_template = """
    A patient has provided their medication history as follows: {history}. We have recommended a specific drug, which has these important medical considerations: {warning}. 

    First, check if the patient's medical history contains any conditions that match the warnings associated with this drug. If there is a match, return 'YES'; otherwise, return 'NO'.

    Second, determine if the medical considerations mention that the drug is classified as a vaccine. If the drug is referred to as a vaccine, return 'YES'; otherwise, return 'NO'.

    If either of the above conditions returns 'YES', the final output should be 'YES'. If both conditions return 'NO', the final output should be 'NO'.

    Output should strictly be 'YES' or 'NO'.
"""


                             
                    summary_prompt_template = PromptTemplate(
                                    input_variables=["history", "warning"], template=summary_template
                                )

                    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
                    chain = LLMChain(llm=llm, prompt=summary_prompt_template)


                    res = chain.invoke(input = {"history":history, "warning" : warning})
                    if res["text"].lower() == 'no':
                                        oo = testrun_drug(query,i)
                                        return(oo)
                    if res["text"].lower() == 'yes':
                                      i=i+1
                                      j = j+1
        if j == 3 :
                  oo = testrun_drug_warn(query,3)
                  j=0
                  return oo




def login_page():
    st.title('Login to AI Healthcare Response System')
    USERNAME = 'DEV'
    PASSWORD = 'Dev12345'
    ACCOUNT = 'phdsaxs-kib61200'
    DB_NAME = 'HealthResponseSystem'
    WAREHOUSE = 'COMPUTE_WH'
    TABLECONTENT= 'USERDETAILS'

    # Configure connection URL for Snowflake
    conn= snowflake.connector.connect(
         user=USERNAME,
                                password=PASSWORD,
                                account=ACCOUNT,
                                warehouse=WAREHOUSE,
                                database=DB_NAME,
                                schema='PUBLIC',
                                role='ACCOUNTADMIN'
                            )

    cur=conn.cursor()
    sql_query = """SELECT * FROM USERDETAILS"""
    cur.execute(sql_query)
    data_fetch=cur.fetchall()
    df=pd.DataFrame(data_fetch,columns=['Username','Age','Gender','Email','Password','Address','Zipcode','MedicalHistory'])
    print(df)
    #user_name= df['Username'][0]
    #Password= df['Password'][0]
    #zipcode=df['Zipcode'][0]
    #history= df['MedicalHistory'][0]
    username = st.text_input('Username', key='login_username')
    password = st.text_input('Password', type='password', key='login_password')
    col1, spacer, col2 = st.columns([1, 0.000000001, 1])
    with col1:
        if st.button('🔑 Login'):
            user_matches = df[(df['Username'] == username) & (df['Password'] == password)]
            if not user_matches.empty:
                st.success('Login successful!')
                 # Here you can expand what happens on a successful login, e.g., displaying user info, redirecting, etc.
                user_info = user_matches.iloc[0]  # Accessing the first match
                st.session_state.authenticated = True
                st.session_state.current_page = 'about'
                st.session_state['username'] = username 
            else:
                st.error("Login Failed. Please check your credentials.")
    with spacer:
        # The spacer column is intentionally left empty to create space between the buttons
        pass

    with col2:
        if st.button('✍️ Register'):
            st.session_state.authenticated = True

            st.session_state.current_page = 'registration'
         


def show_navigation():
    st.sidebar.title("Navigation")
    if st.sidebar.button('🏠 Home Page'):
        st.session_state.current_page = 'about'
    if st.sidebar.button('✍️ Text Assistant'):
        st.session_state.current_page = 'textassistant'
    if st.sidebar.button('🎤 Voice Assistant'):
        st.session_state.current_page = 'voiceassistant'
    if st.sidebar.button('📊 Report'):
        st.session_state.current_page = 'report'
    if st.sidebar.button('⚙️ Settings'):
        st.session_state.current_page = 'settings'
    if st.sidebar.button('🚪 Logout'):
            # Reset authenticated state and go back to login
            st.session_state.authenticated = False
            st.session_state.current_page = 'login'



def about():
    st.title("AI-Enhanced Healthcare Response System")
    st.header("Integration with Pharmacy Services")
    st.write("""
    The system's integration with leading pharmacy services like CVS enables users to directly purchase recommended medications, ensuring alignment with the AI's treatment suggestions. This seamless link not only expedites the acquisition of necessary medications but also enhances the personalized care experience by ensuring that treatments are tailored to each user's specific health conditions.
    """)

    st.header("Continuous Learning and Improvement")
    st.write("""
    One of the system's key features is its ability to continuously learn from user interactions and feedback, improving its performance and predictive accuracy over time. By training the LLM model on vast amounts of medical literature and clinical data, the system can effectively recognize and correlate symptoms with corresponding diseases, facilitating early detection and prompt medical intervention for better health outcomes.
    """)

    st.header("Optimizing Healthcare Delivery")
    st.write("""
    Furthermore, the system addresses challenges faced by the healthcare sector, such as managing vast amounts of medical data and providing personalized care. By offering a seamless, integrated solution that utilizes the power of AI and data management technologies, the system optimizes resource allocation and streamlines healthcare delivery processes, ultimately improving patient outcomes and enhancing overall healthcare efficiency.
    """)

    st.header("Conclusion")
    st.write("""
    Overall, our AI-Enhanced Healthcare Response System represents a significant advancement in healthcare technology, providing users with reliable and personalized health insights, empowering them to take proactive control of their well-being. Through this innovative application, we aim to make healthcare more accessible and improve the quality of life for individuals worldwide.
    """)

def create_sources_string(source_urls):
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = " "
    return sources_string 



def textassistant():
    if "user_prompt_history" not in st.session_state:
        st.session_state["user_prompt_history"] = []

    if "chat_answers_history" not in st.session_state:
        st.session_state["chat_answers_history"] = []
    st.title("AI Healthcare Response System")
    st.subheader("AI Chatbot")
    st.write("Type your symptoms here:")
    text_input = st.text_area("", height=150)
    openai.api_key = os.getenv("OPENAI_API_KEY")
        #ai_response = fetch_ai_response(text_input)
    load_dotenv()
    initialize_pinecone()
    question_text = text_input
    query = question_text
    if st.button('✅ Submit'):
        with st.spinner("Generating Response"):
            time.sleep(10)
            result = run_llm(query)  # Ensure this function processes the query.
            sources = result


        formatted_response = (
            f"{result} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(query)
        st.session_state["chat_answers_history"].append(formatted_response)

    if st.session_state["chat_answers_history"]:
            
        for index, (generated_response, user_query) in enumerate(zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
        )):
            message(user_query, key=f"user_query_{index}", is_user=True)
            message(generated_response, key=f"generated_response_{index}")

    USERNAME = 'DEV'
    PASSWORD = 'Dev12345'
    ACCOUNT = 'phdsaxs-kib61200'
    DB_NAME = 'HealthResponseSystem'
    WAREHOUSE = 'COMPUTE_WH'
    TABLECONTENT= 'USERDETAILS'

    # Configure connection URL for Snowflake
    conn= snowflake.connector.connect(user=USERNAME,
                                                        password=PASSWORD,
                                                        account=ACCOUNT,
                                                        warehouse=WAREHOUSE,
                                                        database=DB_NAME,
                                                        schema='PUBLIC',
                                                        role='ACCOUNTADMIN'
                                                    )

    cur=conn.cursor()
    user_name= st.session_state['username']
    sql_query = """SELECT * FROM "USERDETAILS" Where USERNAME = %s"""
    cur.execute(sql_query,(user_name))
    data_fetch=cur.fetchall()
    df=pd.DataFrame(data_fetch,columns=['Username','Age','Gender','Email','Password','Address','Zipcode', 'MedicalHistory'])

                            # Previous Data (Replace with your actual previous data retrieval logic)
    zipcode= df['Zipcode'][0]
    if zipcode[0].startswith('0'):
         zipcode= zipcode
    else:
         zipcode= "0"+zipcode
                            # Option 4: Provide a direct link
    st.markdown("Check out the [Nearest Pharmacy Store](https://www.cvs.com/store-locator/landing?address="+zipcode+").")        



def voiceassistant():
    st.title("AI Healthcare Response System")
    st.subheader("This is a healthcare response system")
    openai_api_key = os.environ['OPENAI_API_KEY']
        #ai_response = fetch_ai_response(text_input)
    recorded_audio = audio_recorder()
    if recorded_audio:
        audio_file = "audio.mp3"
        with open(audio_file, "wb") as f:
            f.write(recorded_audio)
        
        transcribe_text = transcribe_audio(audio_file)
        st.write("Transcribed Text:", transcribe_text)
        load_dotenv()
        initialize_pinecone()
        question_text = transcribe_text
        query = question_text
        with st.spinner("Generating Response"):
            time.sleep(10)
            result = run_llm(query)  # Ensure this function processes the query.
            st.write(result)

  

def report():
    st.title("User Report")
    st.write('\n')

    col1, col2 = st.columns(2)  # Create two columns for the two plots

    with col1:
        fig = plot()
        st.pyplot(fig)

    with col2:
        fig = word_cloud()  # If you have different data for the second plot, make sure to update this accordingly
        st.pyplot(fig)

    st.write('\n')
    with st.spinner("Generating Response"):
            time.sleep(20)
    try:
        conn = snowflake.connector.connect(
            user='DEV',
            password='Dev12345',
            account='phdsaxs-kib61200',
            warehouse='COMPUTE_WH',
            database='HealthResponseSystem',
            schema='PUBLIC',
            role='ACCOUNTADMIN'
        )

        cur = conn.cursor()
        user_name= st.session_state['username']
        sql_query = """SELECT * FROM "MEDICATIONHISTORY" where Username = %s"""
        cur.execute(sql_query,(user_name))
        data_fetch = cur.fetchall()
        drugdata=pd.DataFrame(data_fetch, columns=['Date', 'DrugName', 'Output','Symptoms', 'Username'])
        
    finally:
        cur.close()
        conn.close()

        # Initialize session state for storing the final report content
    if 'markdown_content' not in st.session_state:
        st.session_state.markdown_content = ""

    summary_template = """
       Generating a report for on {Date}.
       Prescribed Drug: {DrugName}
       Prescription Details: {Output}
       Symptoms Reported: {Symptoms}.
       The report should be detailed in a medical format for each day. Generate it in Markdown Format with and good structure, use sub-heading inplace of heading because the page already has a heading.
    """

    # Your existing logic for OpenAI and environmental variables
    openai_api_key = os.environ['OPENAI_API_KEY']
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

    # Function to generate a summary for each row
    def generate_summary(row):
        summary_prompt = summary_template.format(
           # Username=row['Username'],
            Date=row['Date'],
            DrugName=row['DrugName'],
            Output=row['Output'],
            Symptoms=row['Symptoms']
        )
        
        prompt = PromptTemplate(input_variables=["information"], template=summary_prompt)
        chain = LLMChain(llm=llm, prompt=prompt)
        res = chain.invoke(input={"information": row.to_dict()})
        return res.get('text', 'No content available.')

    # Generate and display the report
    for index, row in drugdata.iterrows():
        summary = generate_summary(row)
        st.session_state.markdown_content += "\n" + summary
    st.write('\n')

    # Assuming you want to display the final report
    st.write(st.session_state.markdown_content)




def  settings(): 
        st.title("Settings Page")
   
        USERNAME = 'DEV'
        PASSWORD = 'Dev12345'
        ACCOUNT = 'phdsaxs-kib61200'
        DB_NAME = 'HealthResponseSystem'
        WAREHOUSE = 'COMPUTE_WH'
        TABLECONTENT= 'USERDETAILS'

        # Configure connection URL for Snowflake
        conn= snowflake.connector.connect(
            user=USERNAME,
                                    password=PASSWORD,
                                    account=ACCOUNT,
                                    warehouse=WAREHOUSE,
                                    database=DB_NAME,
                                    schema='PUBLIC',
                                    role='ACCOUNTADMIN'
                                )

        cur=conn.cursor()
        user_name= st.session_state['username']
        sql_query = """SELECT * FROM "USERDETAILS" where Username = %s"""
        cur.execute(sql_query,(user_name))
        data_fetch=cur.fetchall()
        df=pd.DataFrame(data_fetch,columns=['USERNAME','Age','Gender','Email','Password','Address','Zipcode','MedicalHistory'])

        # Previous Data (Replace with your actual previous data retrieval logic)
        previous_username = df['USERNAME'][0]

        # Update Username
        st.subheader("Update Username")
        new_username = st.text_input("Enter your new username", "")
            
        

        st.subheader("Update Email")
        new_email = st.text_input("Enter your new email", "")
        

        st.subheader("Update Age")
        new_age= st.text_input("Enter your new age", "")
            

        # Update Password
        st.subheader("Update Password")
        new_password = st.text_input("Enter your new password", "", type="password")
        

        # Update Address
        st.subheader("Update Address")
        new_address = st.text_input("Enter your new address", "")
        
        st.subheader("Update Gender")
        new_gender = st.text_input("Enter your new gender", "")
        
        st.subheader("Update Zipcode")
        new_zipcode = st.text_input("Enter your new zipcode", "")

        st.subheader("Update History")
        new_history = st.text_input("Enter your new medical history", "")


        if st.button('✅ Update'):

            if new_username=="":
                st.error("Username cannot be null")

            if new_email=="":
                st.error("Email cannot be null")

            if new_age=="":
                st.error("Email cannot be null")
            if new_password=="":
                st.error("Password cannot be null")

            if new_address=="":
                st.error("Address cannot be null")
            if new_gender=="":
                st.error("Gender cannot be null")
            if new_zipcode=="":
                st.error("Zipcode cannot be null")
            if new_history=="":
                st.error("Medical History cannot be null")

            st.success("Successfully updated your details.")
            user_data = {
                                'USERNAME': [new_username],
                                'Age': [new_age],
                                'Gender': [new_gender],
                                'Email': [new_email],
                                'Password': [new_password],
                                'Address': [new_address],
                                'Zipcode': [new_zipcode],
                                'MedicalHistory': [new_history]
                            }
            df = pd.DataFrame(user_data)
                                    
            # Constants for Snowflake
            USERNAME = 'DEV'
            PASSWORD = 'Dev12345'
            ACCOUNT = 'phdsaxs-kib61200'
            DB_NAME = 'HealthResponseSystem'
            WAREHOUSE = 'COMPUTE_WH'
            TABLECONTENT= 'USERDETAILS'
            # Configure connection URL for Snowflake
            conn= snowflake.connector.connect(
                                        user=USERNAME,
                                        password=PASSWORD,
                                        account=ACCOUNT,
                                        warehouse=WAREHOUSE,
                                        database=DB_NAME,
                                        schema='PUBLIC',
                                        role='ACCOUNTADMIN'
                                    )
            cur=conn.cursor()
            cur.execute("""UPDATE USERDETAILS
            SET "USERNAME" = %s, "Age" = %s, "Gender" = %s, "Email" = %s, "Password" = %s, "Address" = %s, "Zipcode" = %s, "MedicalHistory"= %s
            WHERE "USERNAME" = %s;
        """, (new_username, new_age, new_gender, new_email, new_password, new_address, new_zipcode, new_history, previous_username))
            conn.commit()
            cur.close()




def main():
    # Login Page
    if not st.session_state.authenticated:
        login_page()
    elif st.session_state.current_page == 'registration':
        registration()
    else:
        show_navigation()
        # Display the selected page
        if st.session_state.current_page == 'about':
            st.session_state.markdown_content = ""
            about()
        elif st.session_state.current_page == 'textassistant':
            st.session_state.markdown_content = ""
            textassistant()
        elif st.session_state.current_page == 'voiceassistant':
            st.session_state.markdown_content = ""
            voiceassistant()
        elif st.session_state.current_page == 'report':
            st.session_state.markdown_content = ""
            report()
        elif st.session_state.current_page == 'settings':
            st.session_state.markdown_content = ""
            settings()
       
# The main function call
if __name__ == "__main__":
    main()
