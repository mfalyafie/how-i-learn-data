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
            
            q1 = SelectData(
            '''
            select 
                    date_trunc('month', tt.date) as month ,
                    count(*) as num_threats
                from
                    threat_title tt
                inner join
                    validasi_title vt
                        on
                    tt.id_validasi = vt.id
                where
                    vt.title = 'Valid'
                group by
                    date_trunc('month', tt.date)
                order by
                    month asc
            ;
            '''
            )
            q1_answer = q1.read()
            print(q1_answer)
            print('success query finance data')

        except:
            
            print('not success query')
        
        #business request 2
        try:
            
            q2 = SelectData(
            '''
            select 
                    date_trunc('month', tt.date) as month ,
                    count(*) as num_threats
                from
                    threat_title tt
                inner join
                    validasi_title vt
                        on
                    tt.id_validasi = vt.id
                where
                    vt.title = 'Not Valid'
                group by
                    date_trunc('month', tt.date)
                order by
                    month asc
            ;
            '''
            )
            q2_answer = q2.read()
            print(q2_answer)
            print('success query sales data')

        except:
            
            print('not success query')

        #try business request 3
        try:
            
            q3 = SelectData(
            '''
            select
                    tt.server_id ,
                    st.title ,
                    count(*) as num_threats
            from
                    threat_title tt
            inner join
                    server_title st
                        on
                    tt.server_id = st.id
            group by
                    tt.server_id ,
                    st.title
            order by
                    num_threats desc
            limit 1
            ;
            '''
            )
            q3_answer = q3.read()
            print(q3_answer)
            print('success query sales data')

        except:
            
            print('not success query')

        #business request 4
        try:
            
            q4 = SelectData(
            '''
            with cte as(
                select
                    tt.title ,
                    date_trunc('month', tt.date) as month ,
                    count(*) as num_threats ,
                    rank() over (
                        partition by date_trunc('month', tt.date)
                        order by count(*) desc
                    ) as threat_rank
                from
                    threat_title tt
                group by
                    tt.title ,
                    date_trunc('month', tt.date)
            )

            select
                cte.title ,
                cte.month ,
                cte.num_threats
            from
                cte
            where cte.threat_rank = 1
            order by
                cte.month asc
            ;
            '''
            )
            q4_answer = q4.read()
            print(q4_answer)
            print('success query sales data')

        except:
            
            print('not success query')
        
        #business request 5
        try:
            
            q5 = SelectData(
            '''
            select
                date_part('year', st.date) as year ,
                count(*) as num_servers
            from
                server_title st
            inner join
                status_server ss
                    on
                st.status = ss.id
            where
                date_part('year', st.date) in (2010, 2014)
                and
                ss.title = 'Active'
            group by
                date_part('year', st.date)
            order by
                year asc
            ;
            '''
            )
            q5_answer = q5.read()
            print(q5_answer)
            print('success query sales data')

        except:
            
            print('not success query')

       
        