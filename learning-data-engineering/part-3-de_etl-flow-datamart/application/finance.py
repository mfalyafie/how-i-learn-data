"""
    author: m.fauzanalyafie@gmail.com
    project: ETL core from MongoDB AWS to RDS PostgreSQL
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
from . select import SelectData
pd.options.display.float_format = '{:,.2f}'.format

#Create class and function to read and move csv to datamart(postgresql)

class Finance:

    def datamart(self):
        
        #function for loading environment
        load_dotenv()

        #define env
        
        PASSWORD = os.environ['pas']
        USERPG = os.environ['usrpg']
        PORT = os.environ['port']
        DB = os.environ['db']

        #try read data csv both revenue and trx
        
        try:
            
            monthly_data = SelectData(
            '''
            with cte as(
                select
                    *
                from
                    revenue r
                inner join
                    trx t
                        on
                    r.advertiser_id = t.advertiser
            )

            select
                date_trunc('month', cte.date) as month ,
                sum(cte.price * unit * code) as monthly_revenue
            from
                cte
            group by
                date_trunc('month', cte.date)
            order by month asc
            ;
            '''
            )
            df = monthly_data.read()
            print(df)
            pd_monthly = pd.DataFrame(df)
            print('success query finance data')
            print(pd_monthly)
            print(pd_monthly.info())

        except:
            
            print('not success query')
        
        #try connecting to database staging
        try:

          engine = create_engine('postgresql://{USRPG}:{PASSWORD}@database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(
              USRPG = USERPG, PASSWORD = PASSWORD, PORT = PORT, DB =DB))
          print('success connect database staging')

        except:

          print('failed to connect to database staging')
        
        #try inserting monthly revenue data to datamart for finance

        try:

            pd_monthly.to_sql('finance', engine, if_exists = 'append', index = False)
            print('success insert monthly data to finance')
        
        except:

            print('failed to insert monthly data to finance')