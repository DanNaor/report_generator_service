#!/usr/local/bin/python
from typing import Collection 
from pymongo import MongoClient, mongo_client
import json


import logging
def _setup_logger():    
        logger=logging.getLogger("db_handler")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
logger=_setup_logger()

mongo_client=MongoClient(host='my_mongo',port=27017)
db=mongo_client["json_docs"]
logger.info("uploading json file...")
Collection_TestResult=db["TestResult"]
with open('simple_json.json') as f:
    file_data = json.load(f)
Collection_TestResult.insert_one(file_data)
logger.info("json file uploaded")
mongo_client.close()