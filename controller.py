#!/usr/bin/python
from pymongo import MongoClient
import pika
from minio import Minio
import logging
import uuid
class create_result_instruction(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='my_rabbit'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='controller2RGq',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body="WORK!")
        while self.response is None:
            self.connection.process_data_events()
        return self.response
def _setup_logger():    
        logger=logging.getLogger("controller")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
logger=_setup_logger()
logger.info("creating request....")
create_result_instruction_rpc=create_result_instruction()
logger.info("created request now im calling")
response=create_result_instruction_rpc.call()  
logger.info(response)  
    

