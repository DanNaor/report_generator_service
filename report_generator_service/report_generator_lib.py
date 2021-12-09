#!/usr/local/bin/python
from pymongo import MongoClient
from minio import Minio
import pika
import logging
from bson.json_util import dumps
def _setup_logger():    
        logger=logging.getLogger("controller")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
logger=_setup_logger()
def create_pdf_and_upload():
    # black box for now
    client = MongoClient('localhost', 27017)
    mydatabase = client.name_of_the_database
    collection_name = mydatabase.name_of_collection
    cursor = collection_name.find()
    list_cur = list(cursor)
    json_data = dumps(list_cur)
    
    return "json_data"
def on_request(ch, method, props, body):
  # if body=="WORK!":
    logger.info("sending rpc...")
    response = create_pdf_and_upload()
    ch.basic_publish(exchange='',
    routing_key=props.reply_to,
    properties=pika.BasicProperties(correlation_id = \
    props.correlation_id),
    body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)