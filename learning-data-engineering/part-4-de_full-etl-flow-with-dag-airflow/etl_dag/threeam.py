"""
   author : m.fauzanalyafie@gmail.com
"""

from airflow.operators.bash_operator import BashOperator # type: ignore
from airflow import DAG # type: ignore
from datetime import datetime
import os
import sys


args = {
  'owner': 'airflow'
  , 'start_date': datetime(2022, 7, 15)
  , 'provide_context': True
}

dag = DAG(
  'update-datamart-at-3-am'
  , start_date = datetime(2022, 7, 15)
  , schedule_interval = '0 3 * * *'
  , default_args = args
)


task = BashOperator(
    task_id='update-datamart-at-3-am',
    bash_command='python3 /home/airflow-webserver/G2_2nd_Test/etl_datamart/main.py',
    dag=dag
)
