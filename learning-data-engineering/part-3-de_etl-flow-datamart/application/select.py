"""
    author: m.fauzanalyafie@gmail.com
    project: ETL core from MongoDB AWS to RDS PostgreSQL
"""

#Import Necessary Libraries

import pandas as pd
import psycopg2 as pg
import datetime
import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from sqlalchemy import create_engine, engine_from_config

#Create class and function for showing data

class SelectData:
    
    def __init__(self, sql_script):
        self.sql_script = sql_script

    def read(self):
        
      #function for loading environment

      load_dotenv()

      #define env

      PASSWORD = os.environ['pas']
      USERPG = os.environ['usrpg']
      PORT = os.environ['port']
      DB = os.environ['db']

      #try connecting to database staging
      try:

          engine = create_engine('postgresql://{USRPG}:{PASSWORD}@database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(
              USRPG = USERPG, PASSWORD = PASSWORD, PORT = PORT, DB =DB))
          print('success connect database staging')

      except:

          print('failed to connect to database staging')

      # query

      query = """
              {}
              """.format(self.sql_script)

      # fungsi untuk query ke database

      result = pd.read_sql(query, engine)

      # menampilkan data dari query tsb

      return(result)

      # create dest ip
      #engine_one = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

      # to table
      #data.to_sql("customer", engine_one, if_exists='append', index=False)