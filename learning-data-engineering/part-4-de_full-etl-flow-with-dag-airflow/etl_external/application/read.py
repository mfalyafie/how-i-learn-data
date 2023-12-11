"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from external data csv to RDS PostgreSQL
"""

#Import necessary libraries and set the display
import pandas as pd
import psycopg2 as pg
import datetime
import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from sqlalchemy import create_engine, engine_from_config
pd.options.display.float_format = '{:,.2f}'.format

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

        #create absolute directory to store data csv
        directory = 'data'

        #get current directory
        cwd = os.getcwd()

        #create directory data
        path = os.path.join(cwd, directory)

        #create folder data
        try:
            os.mkdir(path)
            print('success create directory')
        
        except:
            print('cannot create directory')
        
        #try read data csv both revenue and trx
        
        try:
            
            external_claim = pd.read_csv('/Users/alyafie/G2_2nd_Test/etl_external/data/external_claim.csv')
            external_status_info = pd.read_csv('/Users/alyafie/G2_2nd_Test/etl_external/data/external_status_info.csv')
            claim_process = pd.read_csv('/Users/alyafie/G2_2nd_Test/etl_external/data/claim_process.csv')
            internal_status_info = pd.read_csv('/Users/alyafie/G2_2nd_Test/etl_external/data/internal_status_info.csv')
            salesperson = pd.read_csv('/Users/alyafie/G2_2nd_Test/etl_external/data/salesperson.csv')
            claim_process['claim_date'] = pd.to_datetime(claim_process['claim_date'])
            salesperson['join_date'] = pd.to_datetime(salesperson['join_date'])
            print(external_claim)
            print(external_status_info)
            print(claim_process)
            print(internal_status_info)
            print(salesperson)
            print('success read all data')
        
        except:
            
            print('not success read')

        #try connecting database staging
        
        try:
        
            engine = create_engine('postgresql://{USRPG}:{PASSWORD}@database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(
                USRPG = USERPG, PASSWORD = PASSWORD, PORT = PORT, DB =DB))
            print('success connect database staging')
        
        except:
        
            print('failed to connect to database staging')
        
        #try inserting data to respective table

        try:

            external_claim.to_sql('external_claim', engine, if_exists = 'append', index = False)
            external_status_info.to_sql('external_status_info', engine, if_exists = 'append', index = False)
            claim_process.to_sql('claim_process', engine, if_exists = 'append', index = False)
            internal_status_info.to_sql('internal_status_info', engine, if_exists = 'append', index = False)
            salesperson.to_sql('salesperson', engine, if_exists = 'append', index = False)
            print('success insert all data to respective table')
        
        except:

            print('failed to insert some data to respective data')

        