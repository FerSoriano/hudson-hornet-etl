from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from extract_load import extract_and_load

default_args = {
    'owner': 'FerSoriano',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
    "start_date": datetime(2025, 8, 1)
}

with DAG(
    dag_id="etl_suspicious_users",
    default_args=default_args,
    description="ETL process to identify users with multiple credit applications",
    schedule='@daily',
    catchup=False
) as dag:

    run_etl = PythonOperator(
        task_id='load_suspicious_users',
        python_callable=extract_and_load
    )

    run_etl
