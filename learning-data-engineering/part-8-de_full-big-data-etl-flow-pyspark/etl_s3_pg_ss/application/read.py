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
class MoveData:

    def tosql(self):
        
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

        #Create an endpoint
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

        #Get object of all the csv files in s3 bucket
        status_server = endpoint.get_object(
                Bucket = 'g2academy-bucket-yafie-1',
                Key = 'g2_exam3/status_server.csv'
        )

        #Create dataframe using pandas and change it into pyspark dataframe
        df_ss = pd.read_csv(status_server['Body'])
        df_ss = df_ss.dropna()
        print(df_ss)
        
        #sch = StructType([StructField("id", IntegerType()), StructField("server_id", FloatType()),
        #StructField("title", StringType()), StructField("date", DateType()), StructField("id_validasi", IntegerType())])

        df_ss_spark = spark.createDataFrame(df_ss)
        print(df_ss_spark)
        
        df_ss_spark = df_ss_spark.\
            withColumn('id', df_ss_spark.id.cast(IntegerType()))
            
        #Upload the data to pgsql
        try:
            
            df_ss_spark.write.format('jdbc').options(
                url='jdbc:postgresql://database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(PORT = PORT, 
                DB = DB),
                driver='org.postgresql.Driver',
                dbtable='status_server',
                user='{USERPG}'.format(USERPG = USERPG),
                password='{PASSWORD}'.format(PASSWORD = PASSWORD)
            ).mode("overwrite").save()

            print('sucessfully insert data to table')
        
        except:

            print('failed to insert data to table')

