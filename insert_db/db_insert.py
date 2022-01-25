#!/usr/local/bin/python
# this container upload the json files to mongo
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
logger.info("uploading simple json files....")
with open('simple_json.json') as f:
    file_data = json.load(f)
Handler.insert_document('test_result',file_data)

with open('simple_json_fail.json') as f:
    file_data = json.load(f)
Handler.insert_document('test_result',file_data)


logger.info("uploading simple config file....")
with open('global_test_config.json') as f:
    file_data = json.load(f)
Handler.insert_document('config',file_data)


logger.info("json files uploaded")
