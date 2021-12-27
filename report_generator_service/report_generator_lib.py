#!/usr/local/bin/python
# from pymongo import MongoClient
# from minio import Minio
# from bson.json_util import dumps  
# import pandas
from bson.json_util import dumps, loads
import logging
import shutil
from fpdf import FPDF
import pika
from mongo_handler import *
import os

def _setup_logger():    
        logger=logging.getLogger("report_generator")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
logger=_setup_logger()




def create_pdf_and_upload():
  # get test result info from db
   mongo_controller= MongodbHandler()
   testlist=[]
   for data in mongo_controller.get_all_documents("test_result"):
     testlist.append(data)
 #test list is a list that each cell holds a json string that represent a test
  #  logger.info({"test-\n"}+testlist)
   my_lst_str = ''.join(map(str, testlist))
   logger.info("creating pdf...")
   pdf = PDF()
   pdf.add_page()
   pdf.set_font("Arial", size=14)
  
  #  pdf.multi_cell(0, 10, txt=my_lst_str,align="L")
   pdf.output("test_report.pdf") 
   logger.info("created pdf!")      
  #  move pdf to volume
   dst_folder="/app/pdfs"
   src_folder ="/app"
   file_name="test_report.pdf"
   if os.path.isfile(file_name):
      return shutil.move(src_folder +'/'+ file_name, dst_folder +'/'+ file_name)
      

  
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
        self.ln(20)