#!/usr/local/bin/python
# this container upload the json files to mongo
from typing import Collection
from pymongo import MongoClient, mongo_client
import json
from json import dumps, loads
from mongo_handler import MongodbHandler
import logging


def _setup_logger():
    logger = logging.getLogger("db_handler")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    return logger


def upload_json_file(filename, collection_name):
    with open(filename) as f:
        file_data = json.load(f)
    Handler.insert_document(collection_name, file_data)


logger = _setup_logger()
Handler = MongodbHandler()


logger.info("uploading simple json files....")
upload_json_file('simple_json_pass.json', 'TestResults')
upload_json_file('simple_json_fail_1.json', 'TestResults')
upload_json_file('simple_json_fail_2.json', 'TestResults')
upload_json_file('simple_json_fail_3.json', 'TestResults')


upload_json_file('simple_json_fail_4.json', 'TestResults')
upload_json_file('simple_json_fail_5.json', 'TestResults')
upload_json_file('simple_json_fail_6.json', 'TestResults')


logger.info("uploading simple global config file....")
upload_json_file('global_test_config.json', 'Configuration')


logger.info("json files uploaded")
