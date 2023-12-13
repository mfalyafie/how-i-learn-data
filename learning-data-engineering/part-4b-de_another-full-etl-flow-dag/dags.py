from airflow.operators.bash_operator import BashOperator # type: ignore
from airflow import DAG # type: ignore
from datetime import datetime
import os
import sys


args = {
  'owner': 'airflow'
  , 'start_date': datetime(2022, 10, 17)
  , 'provide_context': True
}

dag = DAG(
  'dags_g2_finalproject_de'
  , start_date = datetime(2022, 10, 17)
  , schedule_interval = 'daily'
  , default_args = args
)



task1 = BashOperator(
    task_id='etl_s3_rds',
    bash_command='python3 /home/ubuntu/G2_DE_Final-Project/etl_s3_rds/main.py',
    dag=dag
)


task2 = BashOperator(
    task_id='etl_rds_datamart',
    bash_command='python3 /home/ubuntu/G2_DE_Final-Project/etl_rds_datamart/main.py',
    dag=dag
)

task1 >> task2
