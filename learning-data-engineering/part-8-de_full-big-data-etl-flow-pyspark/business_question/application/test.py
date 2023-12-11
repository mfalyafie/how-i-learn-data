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
class QueryData:

    def fromsql(self):
        
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

       #Business question no. 1
        try:

            q1 = spark.read.format('jdbc').options(
                url='jdbc:postgresql://database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(PORT = PORT, 
                    DB = DB),
                driver='org.postgresql.Driver',
                dbtable="""
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
                """,
                user='{USERPG}'.format(USERPG = USERPG),
                password='{PASSWORD}'.format(PASSWORD = PASSWORD)
            ).load()

            print(q1)

            print('success query')

        except:
            
            print('fail to query')
        
        #Business question no. 2
        try:

            q2 = spark.read.format('jdbc').options(
                url='jdbc:postgresql://database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(PORT = PORT, 
                    DB = DB),
                driver='org.postgresql.Driver',
                dbtable="""
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
                """,
                user='{USERPG}'.format(USERPG = USERPG),
                password='{PASSWORD}'.format(PASSWORD = PASSWORD)
            ).load()

            print(q2)

            print('success query')

        except:
            
            print('fail to query')
        
        #Business question no. 3
        try:

            q3 = spark.read.format('jdbc').options(
                url='jdbc:postgresql://database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(PORT = PORT, 
                    DB = DB),
                driver='org.postgresql.Driver',
                dbtable="""
                select
                    tt.server_id
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
                """,
                user='{USERPG}'.format(USERPG = USERPG),
                password='{PASSWORD}'.format(PASSWORD = PASSWORD)
            ).load()

            print(q3)

            print('success query')

        except:
            
            print('fail to query')
        
        #Business question no. 4
        try:

            q4 = spark.read.format('jdbc').options(
                url='jdbc:postgresql://database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(PORT = PORT, 
                    DB = DB),
                driver='org.postgresql.Driver',
                dbtable="""
                with cte as(
                    select
                        tt.title ,
                        date_trunc('month', tt.date) as month ,
                        count(*) as num_threats ,
                        rank() over (
                            partition by tt.title, date_trunc('month', tt.date)
                            order by count(*) desc
                        ) as threat_rank
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
                """,
                user='{USERPG}'.format(USERPG = USERPG),
                password='{PASSWORD}'.format(PASSWORD = PASSWORD)
            ).load()

            print(q4)

            print('success query')

        except:
            
            print('fail to query')

        #Business question no. 5
        try:

            q5 = spark.read.format('jdbc').options(
                url='jdbc:postgresql://database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(PORT = PORT, 
                    DB = DB),
                driver='org.postgresql.Driver',
                dbtable="""
                select
                    date_part('year', st.date) as year ,
                    count(*) as num_servers
                from
                    server_title st
                inner join
                    server_status ss
                        on
                    st.status = ss.id
                where
                    date_part('year', st.date) in (2010, 2014)
                group by
                    date_part('year', st.date)
                order by
                    year asc
                ;
                """,
                user='{USERPG}'.format(USERPG = USERPG),
                password='{PASSWORD}'.format(PASSWORD = PASSWORD)
            ).load()

            print(q1)

            print('success query')

        except:
            
            print('fail to query')