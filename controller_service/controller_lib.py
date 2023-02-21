#!/usr/local/bin/python
from pymongo import MongoClient, mongo_client
import pika
from minio import Minio
import logging
import uuid
import pymongo
from rabbitmqhandler import RabbitmqHandler
import requests
RMQhendler = RabbitmqHandler()


def _setup_logger():
    logger = logging.getLogger("controller")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    return logger


def create_result_instruction():
    # url = RMQhendler.request_pdf()
    # r= requests.get(url=url)
    return RMQhendler.request_pdf()
