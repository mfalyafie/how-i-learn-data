"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from s3 to RDS MySQL
"""

#Import necessary libraries
import boto3 #type: ignore
import pandas as pd #type: ignore
import os #type: ignore
from dotenv import load_dotenv #type: ignore
import pymysql #type: ignore
from sqlalchemy import create_engine # type: ignore

#Create class and function for creating end point without showing credentials
class MoveData:

    def tosql(self):
        
        # Load and Define env
        load_dotenv()
        ACCESSKEY = os.environ['accesskey']
        SECRETACCESS = os.environ['secretaccess']
        REGION = os.environ['region']
        PASSWORD = os.environ['pas']
        USERMYSQL = os.environ['usrmysql']
        PORT = os.environ['port']
        DB = os.environ['db']

        # Try connecting to AWS S3
        try:
            endpoint = boto3.client(
                    's3',
                    aws_access_key_id = '{}'.format(ACCESSKEY),
                    aws_secret_access_key = '{}'.format(SECRETACCESS),
                    region_name = '{}'.format(REGION)
            )
        
            print('successful connection to s3')

        except:
            
            print('failed to connect to s3')

        # Get the data from S3 bucket: G2_FP_DE
        try:

                merchants = endpoint.get_object(
                        Bucket = 'g2academy-bucket-yafie-1',
                        Key = 'G2_FP_DE/merchants.csv'
                )
                
                products = endpoint.get_object(
                        Bucket = 'g2academy-bucket-yafie-1',
                        Key = 'G2_FP_DE/products.csv'
                )

                product_categories = endpoint.get_object(
                        Bucket = 'g2academy-bucket-yafie-1',
                        Key = 'G2_FP_DE/product_categories.csv'
                )

                order_items = endpoint.get_object(
                        Bucket = 'g2academy-bucket-yafie-1',
                        Key = 'G2_FP_DE/order_items.csv'
                )

                order_details = endpoint.get_object(
                        Bucket = 'g2academy-bucket-yafie-1',
                        Key = 'G2_FP_DE/order_details.csv'
                )
                
                order_summaries = endpoint.get_object(
                        Bucket = 'g2academy-bucket-yafie-1',
                        Key = 'G2_FP_DE/order_summaries.csv'
                )

                discounts = endpoint.get_object(
                        Bucket = 'g2academy-bucket-yafie-1',
                        Key = 'G2_FP_DE/discounts.csv'
                )

                discount_for_merchants = endpoint.get_object(
                        Bucket = 'g2academy-bucket-yafie-1',
                        Key = 'G2_FP_DE/discount_for_merchants.csv'
                )

                print('Successful putting table files into objects')
        
        except:

                print('Failed putting table files into objects')

        # Create dataframe for every single table
        try:

                df_m = pd.read_csv(merchants['Body'])
                print(df_m.head())

                df_p = pd.read_csv(products['Body'])
                print(df_p.head())

                df_pc = pd.read_csv(product_categories['Body'])
                print(df_pc.head())

                df_oi = pd.read_csv(order_items['Body'])
                print(df_oi.head())

                df_od = pd.read_csv(order_details['Body'])
                print(df_od.head())

                df_os = pd.read_csv(order_summaries['Body'])
                print(df_os.head())

                df_d = pd.read_csv(discounts['Body'])
                print(df_d.head())

                df_dfm = pd.read_csv(discount_for_merchants['Body'])
                print(df_dfm.head())

                print('Successfully created dataframe for all tables')

        except:

                print('Failed in creating dataframe for all tables')

        # Move all tables to MySQL
        try:

            # Create connection to AWS RDS MYSQL
            db_connection_str = 'mysql+pymysql://{USERMYSQL}:{PASSWORD}@g2-de-finalproject.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(
                USERMYSQL = USERMYSQL, PASSWORD = PASSWORD, PORT = PORT, DB = DB
            )

            # Create the engine to connect
            db_connection = create_engine(db_connection_str)

            print(db_connection)

            # Move each table to designated table that is already created
            df_m.to_sql('merchants',db_connection, if_exists = 'replace', index = False)
            df_p.to_sql('products',db_connection, if_exists = 'replace', index = False)
            df_pc.to_sql('product_categories',db_connection, if_exists = 'replace', index = False)
            df_oi.to_sql('order_items',db_connection, if_exists = 'replace', index = False)
            df_od.to_sql('order_details',db_connection, if_exists = 'replace', index = False)
            df_os.to_sql('order_summaries',db_connection, if_exists = 'replace', index = False)
            df_d.to_sql('discounts',db_connection, if_exists = 'replace', index = False)
            df_dfm.to_sql('discount_for_merchants',db_connection, if_exists = 'replace', index = False)

            print('successfully move data to MySQL')
        
        except:

            print('failed to move data to MySQL')
