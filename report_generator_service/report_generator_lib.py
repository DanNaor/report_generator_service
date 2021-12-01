#!/usr/bin/python
from pymongo import MongoClient
from minio import Minio
import pika
import logging
def _setup_logger():    
        logger=logging.getLogger("controller")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
logger=_setup_logger()
def create_pdf_and_upload():
    # black box for now
    return "vagina"
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