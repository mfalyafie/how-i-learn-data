# from base64 import decode
# from kafka import KafkaConsumer  # type: ignore
# import json
# import os
# #import logging
# #import sys
# import pandas as pd # type: ignore
# from pandas.io.json import json_normalize # type: ignore


# consumer = KafkaConsumer(
#                 "dbserver1345.inventory.customers",
#                 auto_offset_reset="latest",
#                 group_id=None,
#                 bootstrap_servers=["kafka:9092"],
#                 api_version = (2,0,2),
#                 value_deserializer=lambda x: json.loads(x.decode('utf-8'))
#                 #max_poll_interval_ms=5000,
#                 #max_poll_records=1,
#             )

# for message in consumer:
#     msg = message.value
    
#     df = pd.io.json.json_normalize(msg)    

#     dx = df[["schema.name","payload.before.id","payload.before.first_name","payload.before.last_name","payload.before.email","payload.after.id",
#         "payload.after.first_name","payload.after.last_name","payload.after.email","payload.source.version","payload.op","payload.source.ts_ms"
#     ]]

#     print(dx.head())


"""
   author :m.fauzanalyafie@gmail.com
"""

from application import (
    ReadData
)

if __name__ == '__main__':
    #
    run_data = ReadData()
    #run_data = ReadData()
    run_data.insert()