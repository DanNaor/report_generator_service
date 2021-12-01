#!/usr/bin/python
from pymongo import MongoClient
from minio import Minio
from report_generator_lib import _setup_logger, on_request 
import pika
logger =_setup_logger()
logger.info("connecting server...")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='my_rabbit'))
channel = connection.channel() 
logger.info("connected")
channel.queue_declare(queue='controller2RGq')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='controller2RGq', on_message_callback=on_request)

channel.start_consuming()
