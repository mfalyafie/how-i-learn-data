"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from MongoDB AWS to RDS PostgreSQL
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

#create class and function

class ReadMongo:
 
    def insert(self):
        
        #function for loading environment
        load_dotenv()

        #define env
        URL = os.environ['url']
        USER = os.environ['usr']
        PASSWORD = os.environ['pas']
        USERPG = os.environ['usrpg']
        PORT = os.environ['port']
        DB = os.environ['db']

        #Try connecting to mongodb cloud
        try:
            
            #connect host mongodb cloud
            cluster = MongoClient(
                "mongodb+srv://{USER}:{PASSWORD}@{URL}/?retryWrites=true&w=majority".format(
                    USER = USER ,
                    PASSWORD = PASSWORD ,
                    URL = URL
                )
            )
            
            print('success connect database MongoDB')
        
        except:
        
            print('cannot connect')
    
        #define connection to database
        db = cluster["sample_supplies"]

        #select collections
        sales_data = db.sales

        #query to find data
        query_find_data = {
            "storeLocation": "Seattle" ,
            'purchaseMethod': 'Phone'
        }

        #search data
        data = sales_data.find(query_find_data)

        #print data
        #for x in data:
        #    print(x)
        
        #Create dataframe from mongodb query
        dataframe = pd.DataFrame(data).head()
        print(dataframe)

        #Auto insert to postgre staging database
        try:

            engine = create_engine('postgresql://{USRPG}:{PASSWORD}@database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(
                USRPG = USERPG, PASSWORD = PASSWORD, PORT = PORT, DB =DB))
            print('success connect database staging')

        except:

            print('failed to connect to database staging')

        #dataframe to sql
        try:
        
            dataframe[['storeLocation', 'purchaseMethod']].to_sql('salessuppliesfrommongodb', engine, if_exists = 'append', index = False)
            print('success creating new table in staging database')

        except:
            print('failed to create new table in staging database')

        