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
class ShowData:
    
    def __init__(self, sql_script):
        self.sql_script = sql_script

    def read(self):
        #function for loading environment
        load_dotenv()

        #define env
        URL = os.environ['url']
        USER = os.environ['usr']
        PASSWORD = os.environ['pas']
        USERPG = os.environ['usrpg']
        PORT = os.environ['port']
        DB = os.environ['db']

        try:

            # inisiasi connection
            engine = pg.connect("""
                                    dbname='{DB}'
                                      user='{USERPG}'
                                        host='database.cezaebyc9hil.us-west-1.rds.amazonaws.com'
                                          port='{PORT}'
                                            password='{PASSWORD}'
                                  """.format(
                                    DB = DB, USERPG = USERPG, PORT = PORT, PASSWORD = PASSWORD
                                  )
                              )
            
            print("success connect database rds")

        except:

            print("cannot connect database")

        # query
        query = """
                {}
                """.format(self.sql_script)

        # fungsi untuk query ke database
        result = pd.read_sql(query, engine)

        # menampilkan data dari query tsb
        print(result)
        # create dest ip
        #engine_one = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
        
        # to table
        #data.to_sql("customer", engine_one, if_exists='append', index=False)


        # close connection database
        engine.close()