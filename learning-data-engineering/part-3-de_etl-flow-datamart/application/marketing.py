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

class Marketing:

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
            
            grouping_data = SelectData(
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
                cte.title ,
                sum(cte.price * cte.unit * cte.code) as total_revenue ,
                case 
                    when sum(cte.price * cte.unit * cte.code) between 1 and 500000000 then 'Bronze'
                    when sum(cte.price * cte.unit * cte.code) between 501000000 and 1000000000 then 'Silver'
                    when sum(cte.price * cte.unit * cte.code) > 1000000000 then 'Gold'
                end as level
            from
                cte
            group by
                cte.title
            ;
            '''
            )
            df = grouping_data.read()
            print(df)
            pd_grouping = pd.DataFrame(df)
            print('success query finance data')
            print(pd_grouping)
            print(pd_grouping.info())

        except:
            
            print('not success query')

        #try connecting to database staging
        try:

            engine = create_engine('postgresql://{USRPG}:{PASSWORD}@database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(
                USRPG = USERPG, PASSWORD = PASSWORD, PORT = PORT, DB =DB))
            print('success connect database staging')

        except:

            print('failed to connect to database staging')
        
        #try inserting revenue data to respective table

        try:

            pd_grouping.to_sql('marketing', engine, if_exists = 'append', index = False)
            print('success insert grouping data to datamart marketing')
        
        except:

            print('failed to insert grouping data to datamart marketing')