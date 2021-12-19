#!/usr/local/bin/python
from typing import Collection 
from pymongo import MongoClient, mongo_client
import json
from json import dumps, loads
from mongo_handler import MongodbHandler
import logging
def _setup_logger():    
        logger=logging.getLogger("db_handler")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
logger=_setup_logger()
Handler=MongodbHandler()
logger.info("uploading json file....")
with open('simple_json.json') as f:
    file_data = json.load(f)
Handler.insert_document('test_result',file_data)
# Collection_TestResult.insert_one(file_data)
logger.info("json file uploaded")
