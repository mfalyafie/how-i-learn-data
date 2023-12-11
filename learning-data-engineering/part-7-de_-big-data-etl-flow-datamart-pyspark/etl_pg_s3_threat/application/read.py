"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from s3 to RDS PostgreSQL
"""

#Import necessary libraries
import pyspark #type: ignore
from pyspark.sql import SparkSession #type: ignore
import boto3 #type: ignore
import pandas as pd #type: ignore
import os #type: ignore
from dotenv import load_dotenv #type: ignore
from pyspark.sql.types import * #type: ignore

#Create class and function for creating end point without showing credentials
class SQL:

    def query(self):
        
        #Create spark session on server
        spark = SparkSession.builder\
                    .master("local")\
                    .appName("Exam3")\
                    .config('spark.driver.extraClassPath', '/opt/spark/jars/postgresql-42.3.6.jar')\
                    .getOrCreate()
        
        #function for loading environment
        load_dotenv()

        #define env

        ACCESSKEY = os.environ['accesskey']
        SECRETACCESS = os.environ['secretaccess']
        REGION = os.environ['region']
        PASSWORD = os.environ['pas']
        USERPG = os.environ['usrpg']
        PORT = os.environ['port']
        DB = os.environ['db']

        #sch = StructType([StructField("id", IntegerType()), StructField("server_id", FloatType()),
        #StructField("title", StringType()), StructField("date", DateType()), StructField("id_validasi", IntegerType())])
    
        #Read the data from pgsql
        try:
            
            threat_sql = spark.read.format('jdbc').options(
                url='jdbc:postgresql://database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(PORT = PORT, 
                DB = DB),
                driver='org.postgresql.Driver',
                dbtable='threat_tugas16',
                user='{USERPG}'.format(USERPG = USERPG),
                password='{PASSWORD}'.format(PASSWORD = PASSWORD)
            ).load()

            print('sucessfully read data from pg')
        
        except:

            print('failed to read data from pg')
        
        threat_sql.show()
        threat_sql = threat_sql.dropna()
        threat_sql.show()

