#!/usr/local/bin/python
from report_generator_lib import logger, on_request 
import pika
import os

logger.info("connecting rmq...")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RMQ_HOST")))
channel = connection.channel()
logger.info("connected")
channel.queue_declare(queue='pdfs')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='pdfs', on_message_callback=on_request)
# logger.info("waiting for contoller.... 15 sec be patiant(:")
channel.start_consuming()
