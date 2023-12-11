"""
    author: m.fauzanalyafie@gmail.com
    project: ETL core from MongoDB AWS to RDS PostgreSQL
"""

#Import necessary libraries
import pandas as pd
import psycopg2 as pg
import datetime
import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from sqlalchemy import create_engine, engine_from_config

#Create class and function to read and move csv to datamart(postgresql)

class ReadData:

    def insert(self):
        
        #function for loading environment
        load_dotenv()

        #define env
        
        PASSWORD = os.environ['pas']
        USERPG = os.environ['usrpg']
        PORT = os.environ['port']
        DB = os.environ['db']

        #try read data csv both revenue and trx
        
        try:
            
            revenue_data = pd.read_csv('staging.revenue.csv')
            trx_data = pd.read_csv('staging.trx.csv')
            print(revenue_data.head())
            print(trx_data.head())
            print('success read trx and revenue data')
        
        except:
            
            print('not success read')

        #try creating dataframe for revenue and trx data plus checking the data type

        try:

            df_revenue = pd.DataFrame(revenue_data)
            df_trx = pd.DataFrame(trx_data)
            print(df_revenue.info())
            print(df_trx.info())
            print(df_revenue)
            print(df_trx)
            print('success create dataframe for revenue and trx data')

        except:

            print('failed to create dataframe')

        #try connecting database staging
        
        try:
        
            engine = create_engine('postgresql://{USRPG}:{PASSWORD}@database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(
                USRPG = USERPG, PASSWORD = PASSWORD, PORT = PORT, DB =DB))
            print('success connect database staging')
        
        except:
        
            print('failed to connect to database staging')
        
        #try inserting revenue data to respective table

        try:

            df_revenue.to_sql('revenue', engine, if_exists = 'append', index = False)
            print('success insert revenue data to staging')
        
        except:

            print('failed to insert revenue data to staging')

        #try inserting trx data to respective table

        try:

            df_trx.to_sql('trx', engine, if_exists = 'append', index = False)
            print('success insert trx data to staging')
        
        except:

            print('failed to insert trx data to staging')


        