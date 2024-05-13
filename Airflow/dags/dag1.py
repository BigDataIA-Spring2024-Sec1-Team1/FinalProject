from airflow import DAG, task
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import boto3


s3 = boto3.client("s3")

# Initialize Base URLs
BASE_URL =  'https://www.drugs.com'
DRUG_INFO_URL = f'{BASE_URL}/drug_information.html'

aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

session = boto3.Session(
    aws_access_key_id= aws_access_key_id, #kept blank due to privacy issue,
    aws_secret_access_key=aws_secret_access_key,#kept blank due to privacy issue,
)


s3 = session.client('s3')

def geturg(url):
    # Base URL of the website
    base_url = 'https://www.drugs.com'

    # Specific page to scrape
    url = url

    # Fetch the page
    response = requests.get(url)
    final_urls =[]

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific unordered list by class
        ul = soup.find('ul', class_='ddc-list-column-2')

        # Check if the unordered list was found
        if ul:
            # Find all 'a' tags within the unordered list
            links = ul.find_all('a')

            # Iterate over each link and print the full URL
            for link in links:
                full_url = f"{base_url}{link['href']}"
                final_urls.append(full_url)
                print(f"{link.text}: {full_url}")
        else:
            print("Unordered list element not found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return final_urls

def fetch_navigation_urls():
    response = requests.get(DRUG_INFO_URL)
    full_urls = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        nav = soup.find('nav', class_='ddc-paging')
        if nav:
            links = nav.find_all('a')
            full_urls = [f"{BASE_URL}{link['href']}" for link in links]
    return full_urls

def fetch_detailed_urls(ti):
    navigation_urls = ti.xcom_pull(task_ids='fetch_navigation_urls')
    second_urls = []
    for url in navigation_urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            nav = soup.find('nav', class_='ddc-paging ddc-mgb-2')
            if nav:
                list_items = nav.find_all('li')
                for item in list_items:
                    link = item.find('a')
                    if link:
                        full_url = f"{BASE_URL}{link['href']}"
                        second_urls.append(full_url)
    return second_urls


def finall(url):
    response = requests.get(url)
    df = pd.DataFrame(columns=['Drug_Name', 'Symptoms', 'Dosage', 'Warning'])

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the <h1> tag and extract its text
        h1_tag = soup.find('h1')
        title = h1_tag.text.strip() if h1_tag else 'No title found'

        # Find the <h2> tag with id 'uses'
        h2_uses = soup.find('h2', id='uses')
        h2_dosage = soup.find('h2', id='dosage')
        h2_warning = soup.find('h2', id='before-taking')
        if not h2_dosage:
            h2_dosage = soup.find('h2', id='directions')


        # Initialize a list to hold the text from each <p> tag
        paragraphs_text = []
        paragraphs_dosage = []
        paragraphs_warning = []


        # Check if the <h2> tag was found
        if h2_uses:
            # Find all next siblings
            for sibling in h2_uses.find_next_siblings():
                if sibling.name == 'p':
                    paragraphs_text.append(sibling.text.strip())
                elif sibling.name == 'h2':
                    # Break the loop if it is an <h2> tag with the specific class
                    break
                else:
                    # Skip to the next sibling
                    continue
        if h2_warning:
            # Find all next siblings
            for sibling in h2_warning.find_next_siblings():
                if sibling.name == 'p':
                    paragraphs_warning.append(sibling.text.strip())
                elif sibling.name == 'h2':
                    # Break the loop if it is an <h2> tag with the specific class
                    break
                else:
                    # Skip to the next sibling
                    continue
        if h2_dosage:
            # Find all next siblings
            for sibling in h2_dosage.find_next_siblings():
                if sibling.name == 'p':
                    paragraphs_dosage.append(sibling.text.strip())
                elif sibling.name == 'h2':
                    # Break the loop if it is an <h2> tag with the specific class
                    break
                else:
                    # Skip to the next sibling
                    continue

        # Add each paragraph text to the DataFrame with the corresponding URL and title
        for i in range(max(len(paragraphs_text), len(paragraphs_dosage), len(paragraphs_warning))):
            # Use indexing to access elements if available, else default to an empty string
            symptom = paragraphs_text[i] if i < len(paragraphs_text) else ''
            dosage = paragraphs_dosage[i] if i < len(paragraphs_dosage) else ''
            warning = paragraphs_warning[i] if i < len(paragraphs_warning) else ''

            # Append the row to the DataFrame
            new_row = pd.DataFrame([{'Drug_Name': title, 'Symptoms': symptom, 'Dosage': dosage, 'Warning': warning}])
            df = pd.concat([df, new_row], ignore_index=True)


        return df

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return df



def scrape_drug(ti):
    detailed_urls = ti.xcom_pull(task_ids='fetch_detailed_urls')
    all_final_urls = []
    for url in detailed_urls:
        urls_from_page = geturg(url)
        all_final_urls.extend(urls_from_page)
        ti.xcom_push(key='final_urls', value=all_final_urls)

def scrape_drug_info(ti):
    detailed_urls = ti.xcom_pull(task_ids='scrape_drug', key='final_urls')
    first_1000_urls = detailed_urls
    time.sleep(300)
    df = pd.DataFrame()
    i = 0
    j=0
    for url in first_1000_urls:
       new_df = finall(url)  # Get the DataFrame from each URL
       if not new_df.empty:
            if i == 0:
                df = new_df
                i = i+1# If first URL, assign directly
            else:
                df = pd.concat([df, new_df])
                i = i+1
                j= j+1
                print(i)
            if j > 800:
                time.sleep(300)
                print('sleep')
                j=0
    

    grouped_df = df.groupby('Drug_Name').agg({
            'Symptoms': ' '.join,  # Aggregate Symptoms into a single string
            'Dosage': ' '.join,    # Aggregate Dosage instructions
            'Warning': ' '.join    # Aggregate Warnings
        }).reset_index()
    print(grouped_df.head())
    filename = "Mark1.csv"
    grouped_df.to_csv(filename, index=False)  
    with open(filename, "rb") as f:
        s3.upload_fileobj(f, S3_BUCKET_NAME, filename)




  
       
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 11, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    dag_id='scrape_drug_info',
    default_args=default_args,
    description='Scrape drug information from drugs.com',
    schedule_interval=timedelta(days=30),
    catchup=False  # Set to False if you don't want historical DAG runs to execute
)




trigger = TriggerDagRunOperator(
    task_id = 'trigger_target_dag',
    trigger_dag_id = 'process_csv_data_dag',
    wait_for_completion = True,
    execution_date = '{{ ds }}'

)



task1 = PythonOperator(
    task_id='fetch_navigation_urls',
    python_callable=fetch_navigation_urls,
    dag=dag,
)



task2 = PythonOperator(
    task_id='fetch_detailed_urls',
    python_callable=fetch_detailed_urls,
    provide_context=True,
    dag=dag,
)

task3 = PythonOperator(
    task_id='scrape_drug_info',
    python_callable=scrape_drug_info,
    provide_context=True,
    dag=dag,
)

task4 = PythonOperator(
    task_id='scrape_drug',
    python_callable=scrape_drug,
    provide_context=True,
    dag=dag,
)




task1 >> task2 >> task4 >> task3 
