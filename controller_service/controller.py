#!/usr/local/bin/python
from typing import Collection
from controller_lib import _setup_logger, create_result_instruction 
from pymongo import MongoClient, mongo_client
import json
import pika
from minio import Minio
# logger for showing data flow 
logger=_setup_logger()
#telling RG to generate report
logger.info("calling...")
response=create_result_instruction()
logger.info("called waiting for response...")
logger.info("response-\n"+response.decode("utf-8"))  
