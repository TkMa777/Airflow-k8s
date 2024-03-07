from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests


def get_data(**kwargs):
    # URL to file CSV
    url = 'https://raw.githubusercontent.com/TkMa777/k8s-Airflow/master/dags/Sales.csv'
    response = requests.get(url)

    # Checker la request
    if response.status_code == 200:
        df = pd.read_csv(url)
        json_data = df.to_json(orient='records')
        kwargs['ti'].xcom_push(key='data', value=json_data)
    else:
        raise Exception(f'Failed to get data, HTTP status code: {response.status_code}')


# Function to analyze the fetched data
def analyze_data(**kwargs):
    # Retrieve data passed from the previous task
    output_data = kwargs['ti'].xcom_pull(key='data', task_ids='get_data')
    df = pd.read_json(output_data)

    # Ensuring Selling Price is a numeric
    df['Selling Price'] = pd.to_numeric(df['Selling Price'], errors='coerce')

    # Aggregate data by brands
    aggregation_functions = {
        'Selling Price': ['mean', 'max', 'count'],  # AVG, max and model count
        'Models': 'nunique'  # Only unique modeles
    }

    df_aggregated = df.groupby('Brands').agg(aggregation_functions).reset_index()
    df_aggregated.columns = ['Brands', 'Average Selling Price', 'Max Selling Price', 'Models Count',
                             'Unique Models Count']

    # Sort the data by average selling price for better insights
    df_aggregated = df_aggregated.sort_values(by='Average Selling Price', ascending=False)

    print(df_aggregated.head())

    # Pass the aggregated data for potential further use
    kwargs['ti'].xcom_push(key='aggregated_data', value=df_aggregated.to_json(orient='records'))


default_args = {
    'owner': 'Tacho',
    'start_date': datetime(2024, 3, 6),
    'catchup': False
}

# Default DAG arguments
dag = DAG(
    'fetch_analyze',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    tags=['example']
)

# Task definitions
get_data_from_url = PythonOperator(
    task_id='get_data',
    python_callable=get_data,
    dag=dag,
)

analyze_data_task = PythonOperator(
    task_id='analyze_data',
    python_callable=analyze_data,
    dag=dag,
)

# Order of the tasks
get_data_from_url >> analyze_data_task
