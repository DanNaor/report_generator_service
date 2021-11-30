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
logger =_setup_logger()
logger.info("connecting server...")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='my_rabbit'))
channel = connection.channel() 
logging.info("connected")
channel.queue_declare(queue='controller2RGq')

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
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='controller2RGq', on_message_callback=on_request)

channel.start_consuming()
