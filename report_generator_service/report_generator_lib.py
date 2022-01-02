#!/usr/local/bin/python
# from pymongo import MongoClient
# from minio import Minio
# from bson.json_util import dumps  
# import pandas
import re
import logging
import shutil
from fpdf import FPDF
import pika
from mongo_handler import *
import os
from bson.json_util import loads, dumps
def _setup_logger():    
        logger=logging.getLogger("report_generator")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
logger=_setup_logger()

def create_pdf_and_upload():
  # get info from db
   mongo_controller= MongodbHandler()

   config_data_bson=mongo_controller.get_jsonOBJ("global_config")
   json_str = dumps(config_data_bson)
   config_dataOBJ=loads(json_str)
   logger.info("creating pdf...")
   pdf = PDF()
   pdf.add_page()
   logger.info(config_dataOBJ)
   for value in config_dataOBJ:
     pdf.cell(14, h = 6, txt = str(value) +'-'+'\t'+str(config_dataOBJ[value]), border = 0, ln = 30, 
     align = '', fill = False, link = '')
     pdf.ln(5)
   pdf.output("test_report.pdf") 
   logger.info("created pdf!")
   
   return "path-"+move_pdf_2_volume()
 
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

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('Hatal_logo.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Results', 1, 0, 'C')
        # Line break
        self.ln(45)
        
def move_pdf_2_volume():
    #  move pdf to volume
     dst_folder="/app/pdfs"
     src_folder ="/app"
     file_name="test_report.pdf"
     if os.path.isfile(file_name):
        return shutil.move(src_folder +'/'+ file_name, dst_folder +'/'+ file_name)

