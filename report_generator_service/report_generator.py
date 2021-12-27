#!/usr/local/bin/python
from pymongo import MongoClient
from minio import Minio
from report_generator_lib import logger, on_request 
import pika
logger.info("connecting server...")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='my_rabbit'))
channel = connection.channel() 
logger.info("connected")
channel.queue_declare(queue='pdfs')
# need to add commnets!!!!!!!!! 
channel.basic_qos(prefetch_count=1)
logger.info("waiting for contoller.... 10 sec be patiant(:")
channel.basic_consume(queue='pdfs', on_message_callback=on_request)

channel.start_consuming()