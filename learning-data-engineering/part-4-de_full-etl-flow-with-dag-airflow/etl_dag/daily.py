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
  'update-datamart-daily'
  , start_date = datetime(2022, 7, 15)
  , schedule_interval = '@daily'
  , default_args = args
)

#/Users/alyafie/G2_2nd_Test/etl_datamart/main.py
task = BashOperator(
    task_id='update-datamart-daily',
    bash_command='python3 /home/airflow-webserver/G2_2nd_Test/etl_datamart/main.py',
    dag=dag
)
