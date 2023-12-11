"""
    author: m.fauzanalyafie@gmail.com
    project: ETL core from MongoDB AWS to RDS PostgreSQL
"""

import pandas as pd
import psycopg2 as pg
import datetime
import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from sqlalchemy import create_engine, engine_from_config

class ReadData:
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
        

        #create absolute directory to store data csv
        directory = 'storage'
        
        #get current directory
        cwd = os.getcwd()

        #create directory data
        path = os.path.join(cwd, directory)

        #mongodb+srv://falyafie:<password>@cluster0.enggskq.mongodb.net/?retryWrites=true&w=majority
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
        #print('Jalankan!')
    
        #define connection to database
        db = cluster["sample_airbnb"]

        #select collections
        account_data = db.listingsAndReviews

        #query to find data
        query_find_data = {
            "listing_url": 'https://www.airbnb.com/rooms/10006546'
        }

        #search data
        data = account_data.find(query_find_data)

        #print data
        for x in data:
            print(x)
        
        try:
            #filter data
            filter_data = {
                'listing_url': 'https://www.airbnb.com/rooms/10006546'
            }

            #query update
            query_update = {
                '$set': {
                    'listing_url': 'https://www.yafie.com/rooms/10006546'
                }
            }

            update_data = account_data.update_one(filter_data, query_update)

            print('success update data')
        
        except:
            
            print('cannot update data')
        

        #query find data
        query_find_data_update = {
            'listing_url': 'https://www.yafie.com/rooms/10006546'
        }

        #search data
        data_update = account_data.find(
            query_find_data_update
        )

        for xx in data_update:
            print(xx)
        
        #delete data
        try:
            #delete data account_id = 0
            delete_query = {
                'listing_url': 'https://www.yafie.com/rooms/10006546'
            }

            #delete data
            account_data.delete_one(delete_query)

            #success delete data
            print('success delete data')
        
        except:
            #cannot delete data
            print('cannot delete data')
        
        query_find_data_delete = {
            'account_id': 'https://www.yafie.com/rooms/10006546'
        }

        #search data
        data_delete = account_data.find(query_find_data_delete)

        for xxx in data_delete:
            print('check data delete or not')
            print(xxx)

        #dataframe table account
        dataframe = pd.DataFrame(account_data.find())

        #print top 5 data
        print(dataframe.head())
        
        #get current timestamp
        time = datetime.datetime.now()

        #get DD-MM-YYYY HH-MM-S
        xyz = time.strftime('%Y-%M-%d_%H-%M-%S')
        print(xyz)

        #create folder data
        try:
            os.mkdir(path)
            print('success create directory')
        
        except:
            print('cannot create directory')

        try:

            #save dataframe to local data
            dataframe[0:3].to_csv('{cwd}/storage/listreview_et1_{ts}.csv'.format(cwd = cwd, ts = xyz) ,
                                index = False
            )
        
            #print success import to csv
            print('success insert data to csv')
        
        except:
            print('cannot save data')
        
        #read data csv
        data_sql = pd.read_csv('{cwd}/storage/listreview_et1_{ts}.csv'.format(cwd=cwd, ts = xyz))

        print('====print datasql from csv file====')
        print(data_sql.head())

        #inisiasi connect database
        engine = create_engine('postgresql://{USRPG}:{PASSWORD}@database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(
            USRPG = USERPG, PASSWORD = PASSWORD, PORT = PORT, DB =DB ))

        #dataframe to sql
        data_sql.to_sql('tablefromairbnb', engine, if_exists = 'append', index = False)

        #remove data csv
        os.remove('{cwd}/storage/listreview_et1_{ts}.csv'.format(cwd=cwd, ts = xyz))

    


    



    

