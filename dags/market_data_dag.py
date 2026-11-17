
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="market_data_pipeline",
    start_date=datetime(2026, 11, 10),
    schedule="@daily",
    catchup=False,
) as dag:

    extract = BashOperator(
        task_id="extract_market_data",
        bash_command="python /opt/airflow/dags/test_bronze.py"
    )

    transform = BashOperator(
        task_id="transform_market_data",
        bash_command="python /opt/airflow/dags/transform_market_data.py"
    )

    load = BashOperator(
        task_id="load_market_data",
        bash_command="python /opt/airflow/dags/load_market_data.py"
    )

    extract >> transform >> load
