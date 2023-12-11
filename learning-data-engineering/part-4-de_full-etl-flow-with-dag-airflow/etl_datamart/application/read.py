"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from pg to datamart
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
from . query import SelectData
pd.options.display.float_format = '{:,.2f}'.format

#Create class and function to read and move csv to datamart(postgresql)

class Disburse:

    def datamart(self):
        
        #function for loading environment
        load_dotenv()

        #define env
        
        PASSWORD = os.environ['pas']
        USERPG = os.environ['usrpg']
        PORT = os.environ['port']
        DB = os.environ['db']

        #business request 1
        
        try:
            
            monthly_data = SelectData(
            '''
            with cte as (
                select
                    cp.claim_date ,
                    ec.claim ,
                    esi.status
                from
                    claim_process cp
                inner join
                    external_status_info esi
                        on
                    cp.external_status = esi.id
                inner join
                    external_claim ec
                        on
                    cp.insurance_id = ec.id
            )
            select
                date_trunc('month', cte.claim_date) as month ,
                sum(cte.claim) as monthly_claim
            from 
                cte
            where
                cte.status = 'Approve'
            group by
                date_trunc('month', cte.claim_date)
            order by
                month
            '''
            )
            monthly_claim = monthly_data.read()
            print(monthly_claim)
            print('success query finance data')

        except:
            
            print('not success query')
        
        #try connecting to database staging
        try:

          engine = create_engine('postgresql://{USRPG}:{PASSWORD}@database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(
              USRPG = USERPG, PASSWORD = PASSWORD, PORT = PORT, DB =DB))
          print('success connect database staging')

        except:

          print('failed to connect to database staging')
        
        #try inserting monthly claim data to datamart for finance

        try:

            monthly_claim.to_sql('finance_test', engine, if_exists = 'append', index = False)
            print('success insert monthly data to finance')
        
        except:

            print('failed to insert monthly data to finance') 

        #business request 2
        try:
            
            sales_data = SelectData(
            '''
            select
                date_trunc('month', s.join_date) as month ,
                count(*) as monthly_salesperson
            from 
                salesperson s
            group by
                date_trunc('month', s.join_date)
            order by
                month
            '''
            )
            monthly_salesperson = sales_data.read()
            print(monthly_salesperson)
            print('success query sales data')

        except:
            
            print('not success query')

        #try inserting monthly salesperson data to sales datamart
        try:

            monthly_salesperson.to_sql('sales_test', engine, if_exists = 'append', index = False)
            print('success insert monthly data to sales')
        
        except:

            print('failed to insert monthly data to sales') 

        #try business request 3
        try:
            
            legal_data = SelectData(
            '''
            with cte as (
                select
                    cp.reason ,
                    isi.status ,
                    cp.id
                from
                    claim_process cp
                inner join
                    internal_status_info isi
                        on
                    cp.internal_status = isi.id               
            )

            select
                cte.reason ,
                cte.status ,
                count(*) as num_reason_status
            from 
                cte
            group by
                cte.reason ,
                cte.status
            '''
            )
            legal_reason = legal_data.read()
            print(legal_reason)
            #print('success query sales data')

        except:
            
            print('not success query')

        #try inserting monthly salesperson data to sales datamart
        try:

            legal_reason.to_sql('legal_test', engine, if_exists = 'append', index = False)
            print('success insert legal data to legal')
        
        except:

            print('failed to insert monthly data to legal') 
       
        