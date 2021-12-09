from typing import Collection
from controller_lib import _setup_logger, create_result_instruction 
from pymongo import MongoClient, mongo_client
import json
import pika
from minio import Minio
import logging
# logger for showing data flow 
logger=_setup_logger()

# connecting to mongodb
mongo_client=MongoClient(host='my_mongo',port=27017)
db=mongo_client["json_docs"]

logger.info("json file uploaded")
logger.info("creating request....")
create_result_instruction_rpc=create_result_instruction()
logger.info("created request now im calling")
logger.info("uploading json file...")
Collection_TestResult=db["TestResult"]
with open('simple_json.json') as f:
    file_data = json.load(f)
Collection_TestResult.insert_one(file_data)
response=create_result_instruction_rpc.call()  
logger.info(response)  
mongo_client.close()