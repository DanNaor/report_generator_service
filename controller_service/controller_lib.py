#!/usr/local/bin/python
from pymongo import MongoClient, mongo_client
import pika
from minio import Minio
import logging
import uuid
import pymongo
from rabbitmqhandler import RabbitmqHandler
RMQhendler = RabbitmqHandler()


def _setup_logger():
    logger = logging.getLogger("controller")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    return logger


def create_result_instruction():
    return RMQhendler.request_pdf()
