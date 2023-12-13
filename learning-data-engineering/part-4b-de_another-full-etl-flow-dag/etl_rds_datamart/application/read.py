"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from pg to datamart
"""

#Import necessary libraries and set the display
import pandas as pd
import pymysql #type: ignore
import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, engine_from_config
from . query import Query
pd.options.display.float_format = '{:,.2f}'.format

#Create class and function to read and move csv to datamart(postgresql)

class Disburse:

    def datamart(self):
        
        #function for loading environment
        load_dotenv()

        #define env
        
        PASSWORD = os.environ['pas']
        USERMYSQL = os.environ['usrmysql']
        PORT = os.environ['port']
        DB = os.environ['db']
        DBMART = os.environ['dbmart']

        #business request 1
        
        try:

            q1 = Query(
            '''
            WITH co as (
                SELECT
                    os.merchant_id,
                    count(1) as num_co_trx
                FROM
                    order_summaries os
                GROUP BY
                1
            ),
            pu as (
                SELECT
                    p.merchant_id,
                    count(1) as num_product_created
                FROm
                products p
                GROUP BY
                1
            ),
            pcu as (
                SELECT
                    pc.merchant_id,
                    count(1) as num_product_cat_created
                FROM
                    product_categories pc
                GROUP BY
                1
            ),
            du as (
                SELECT
                    dfm.merchant_id,
                    count(1) as num_discount_created
                FROM
                    discounts d
                INNER JOIN
                    discount_for_merchants dfm
                        ON
                    d.id = dfm.discount_id
                WHERE d.owner = 'MERCHANT'
                GROUP BY
                1
            )
            SELECT
                m.id,
                co.num_co_trx,
                pu.num_product_created,
                pcu.num_product_cat_created,
                du.num_discount_created,
                IF(co.num_co_trx > 15, 1, 0) as co_fluent,
                IF(pu.num_product_created >= 5, 1, 0) as pu_fluent,
                IF(pcu.num_product_cat_created > 1, 1, 0) as pcu_fluent,
                IF(du.num_discount_created is not null, 1, 0) as du_fluent 
            FROM
                merchants m
            LEFT JOIN
                co
                    ON
                m.id = co.merchant_id
            LEFT JOIN
                pu
                    ON
                m.id = pu.merchant_id
            LEFT JOIN
                pcu
                    ON
                m.id = pcu.merchant_id
            LEFT JOIN
                du
                    ON
                m.id = du.merchant_id
            ORDER BY
            num_co_trx desc
            '''
            )
            q1_answer = q1.mysql()
            print(q1_answer.head())
            print('success query')

        except:
            
            print('not success query')
        
        #business request 2
        try:
            
            q2 = Query(
            '''
            SELECT
                oi.id,
                p.name,
                oi.price
            FROM
                order_items oi
            INNER JOIN
                products p
                    ON
                oi.product_id = p.id
            '''
            )
            q2_answer = q2.mysql()
            print(q2_answer.head())
            print('success query')

        except:
            
            print('not success query')

        #try business request 3
        try:
            
            q3 = Query(
            '''
            SELECT
                d.type,
                d.unit,
                count(d.id) as num_discount
            FROM
                discounts d
            GROUP BY
            1, 2
            '''
            )
            q3_answer = q3.mysql()
            print(q3_answer.head())
            print('success query')

        except:
            
            print('not success query')

        #business request 4
        try:
            
            q4 = Query(
            '''
            SELECT
                os.merchant_id,
                SUM(os.total) as trx_value
            FROM
                order_summaries os
            GROUP BY
            1
            ORDER BY
            2 desc
            '''
            )
            q4_answer = q4.mysql()
            print(q4_answer.head())
            print('success query')

        except:
            
            print('not success query')
        
        #try connecting to database staging
        try:

            engine = create_engine('mysql+pymysql://{USERMYSQL}:{PASSWORD}@g2-de-finalproject.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DBMART}'.format(
                USERMYSQL = USERMYSQL, PASSWORD = PASSWORD, PORT = PORT, DBMART = DBMART))
            
            print('success connect database staging')

        except:

            print('failed to connect to database staging')

        #try inserting monthly salesperson data to sales datamart
        try:

            q1_answer.to_sql('product_usage', engine, if_exists = 'replace', index = False)
            q2_answer.to_sql('price_distribution', engine, if_exists = 'replace', index = False)
            q3_answer.to_sql('discount_distribution', engine, if_exists = 'replace', index = False)
            q4_answer.to_sql('top_merchants', engine, if_exists = 'replace', index = False)
            print('success insert to datamart')
        
        except:

            print('failed to insert to datamart')