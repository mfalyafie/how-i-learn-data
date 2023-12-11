from base64 import decode
from kafka import KafkaConsumer  # type: ignore
import json
import os
#import logging
#import sys
import pandas as pd # type: ignore
from pandas.io.json import json_normalize # type: ignore
from dotenv import load_dotenv
from sqlalchemy import create_engine, engine_from_config

class ReadData:

    def insert(self):
        
        #function for loading environment
        load_dotenv()

        #define env
        
        PASSWORD = os.environ['pas']
        USERPG = os.environ['usrpg']
        PORT = os.environ['port']
        DB = os.environ['db']
        
        consumer = KafkaConsumer(
                        "dbserver1345.inventory.orders",
                        auto_offset_reset="latest",
                        group_id=None,
                        bootstrap_servers=["kafka:9092"],
                        api_version = (2,0,2),
                        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
                        #max_poll_interval_ms=5000,
                        #max_poll_records=1,
                    )

        #try connecting to database staging
        #try:

        engine = create_engine('postgresql://{USRPG}:{PASSWORD}@database.cezaebyc9hil.us-west-1.rds.amazonaws.com:{PORT}/{DB}'.format(
            USRPG = USERPG, PASSWORD = PASSWORD, PORT = PORT, DB =DB))
        #print('success connect database staging')

        #except:

          #  print('failed to connect to database staging')

        for message in consumer:
            msg = message.value
            
            df = pd.io.json.json_normalize(msg)    

            dx = df[["schema.name","payload.before.order_number","payload.before.order_date","payload.before.purchaser","payload.before.quantity", "payload.before.product_id",
            "payload.after.order_number","payload.after.order_date","payload.after.purchaser","payload.after.quantity", "payload.after.product_id"
            ]]

            print(dx.head())
        
            #function for loading environment
            load_dotenv()

            #define env
            
            PASSWORD = os.environ['pas']
            USERPG = os.environ['usrpg']
            PORT = os.environ['port']
            DB = os.environ['db']

            #try inserting monthly claim data to datamart for finance

            try:

                dx.to_sql('sample_orders', engine, if_exists = 'replace', index = False)
                print('success insert sample_addresses')
            
            except:

                print('failed to insert sample_addresses')