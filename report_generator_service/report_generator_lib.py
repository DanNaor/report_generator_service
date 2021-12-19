#!/usr/local/bin/python
# from pymongo import MongoClient
# from minio import Minio
import pika
import logging
# from bson.json_util import dumps  
# import pandas
def _setup_logger():    
        logger=logging.getLogger("report_generator")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
logger=_setup_logger()




def create_pdf_and_upload():
   return "toker super gay"



def on_request(ch, method, props, body): 
  if body!=None:
    logger.info("im in request")
    response =  create_pdf_and_upload()
    ch.basic_publish(exchange='',
    routing_key=props.reply_to,
    properties=pika.BasicProperties(correlation_id = \
    props.correlation_id),
    body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)