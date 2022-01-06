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
from itertools import islice
from minio import Minio
def _setup_logger():    
        logger=logging.getLogger("report_generator")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
logger=_setup_logger()

def create_pdf_and_upload():
  # get info from db
   mongo_controller= MongodbHandler()
  #  the configuration data is a single json doc there for config_data_json will hold a single json doc which hold the data about the global configuration 
   config_data_json=mongo_controller.get_find_one("global_config") 
   #get_all_documents_in_list retruns a list of dic that each dic represent a json document (Test)
   test_result_list= mongo_controller.get_all_documents_in_list("test_result")
   logger.info("creating pdf...")
   pdf = PDF()
  #  config page
   pdf.add_page()
   pdf.cell(80)
   pdf.cell(30, 10, 'Configuration', 0, 0, 'C')
   pdf.line(0,0,pdf.line_width,0)
   pdf.ln(15)
   # Remember to always put one of these at least once.
   pdf.set_font('Courier','',10.0) 
   # Effective page width, or just epw
   epw = pdf.w - 2*pdf.l_margin
   # Set column width to 1/4 of effective page width to distribute content 
   # evenly across table and page
   col_width = epw/2
 
   th = pdf.font_size
  # iterating throught the json file to display the data in the pdf file ,skipping the first field (id)
   for row in islice(config_data_json,1,None):
     pdf.cell(col_width, th, txt =  str(row), border = 1, )
     pdf.cell(col_width, th, txt =  str(config_data_json[row]), border = 1, )
     pdf.ln(th)

  # tests page
   pdf.add_page()
   # moving title to the middle of the file
   pdf.cell(80)
   # displaying title 
   pdf.cell(20,20,txt="Tests-")
   pdf.ln(10)
   #iterating throught the list and displaying the test separately with space between them
   for dic in test_result_list:
     pdf.ln(10)
     for value in islice(dic,1,None):
      pdf.cell(14, h = 6, txt =  re.sub(r"(\w)([A-Z])", r"\1 \2", str(value))  +'-'+'\t'+str(dic[value]), border = 0, ln = 30, 
     align = '', fill = False, link = '')
     pdf.ln(5)
   pdf.add_page()
   pdf.ln(20)
   pdf.cell(80)
   pdf.image('toker_is_a_baddy.png', 60,70, 100)

  # creating the pdf
   pdf.output("test_report.pdf") 
   logger.info("created pdf!")
   logger.info("uploading file to MinIO...")
   # creating a client to have CRUD function with minio
   MinIOclient= getMinoClient()
   # creating a bucket 
   if(not MinIOclient.bucket_exists('pdfbucket')):
     MinIOclient.make_bucket('pdfbucket')
   # getting the pdfs path
   path= move_pdf_2_volume()
   try:
     # getting pdf from container filerstream
    with open(path,'rb') as pdf_file:
      # getting file size
       statdata= os.stat(path)
       # adding file to bucket
       MinIOclient.put_object(
         'pdfbucket',
         'test_report.pdf',
         pdf_file,
         statdata.st_size
       )
   except logging.exception as indentifier:
       return "):"
   logger.info("uploaded file to MinIO")
   return "(:"


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
        self.ln(35)

def getMinoClient():
    return Minio(
      "my_minio:9000",
      access_key=os.getenv('MINIO_ROOT_USER'),
      secret_key=os.getenv('MINIO_ROOT_PASSWORD'),
      secure=False
    )

def move_pdf_2_volume():
    #  move pdf to volume
     dst_folder="/app/pdfs"
     src_folder ="/app"
     file_name="test_report.pdf"
     if os.path.isfile(file_name):
        return shutil.move(src_folder +'/'+ file_name, dst_folder +'/'+ file_name)
