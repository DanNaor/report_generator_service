#!/usr/local/bin/python
import logging
import os
import requests
import pika
import json
from fpdf import FPDF
from mongo_handler import *



def _setup_logger():
    logger = logging.getLogger("report_generator")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    return logger


logger = _setup_logger()

def create_pdf_and_upload():
  # get info from db
    mongo_controller = MongodbHandler()
  #  get the global config data as as a dic(quary by a key name )
    test_config_json = mongo_controller.get_find_one(
        "Configuration", 'ConfigType', 'TestConfig')
    # get_all_documents_in_list returns a list of dic that each dic represent a json document (Test)
    test_result_list = mongo_controller.get_documents_by_location(
        "TestResults")

    logger.info(test_result_list)
    # for item in SortedTestResults:
    #     logger.info(item)
    #     logger.info("   ")
    #     logger.info(SortedTestResults[item])
    logger.info("creating pdf...")
    pdf = PDF()



  #  config page
    pdf.add_page()
    pdf.cell(80)
    pdf.cell(50, 10, 'Configuration:', 1, 0, 'C')
    pdf.line(0, 0, pdf.line_width, 0)
    pdf.ln(20)
    # Remember to always put one of these at least once.
    pdf.set_font('Courier', '', 10.0)
    # Effective page width, or just epw
    epw = pdf.w - 2*pdf.l_margin
    # Set column width to 1/4 of effective page width to distribute content
    # evenly across table and page
    col_width = epw/3
    th = pdf.font_size
  # iterating thought the json file to display the data in the pdf file ,skipping the first field (id)
    for row in test_config_json:
        pdf.set_font('Courier', 'I', 12)
        pdf.cell(col_width, th, txt=str(row), border=0, )
        pdf.set_font('Courier', '', 10.0)
        pdf.cell(col_width, th, txt=str(test_config_json[row]), border=0, )
        pdf.ln(2*th)




  # tests page
    pdf.add_page()
    # moving title to the middle of the file
    pdf.cell(80)
    # displaying title
    pdf.set_font('Courier', 'B', 15)
    pdf.cell(30, 10, 'Tests:', 1, 0, 'C')
    pdf.ln(10)
    # iterating thought the list and displaying the test separately with space between them
    pdf.set_font('Courier', '', 10.0)
    for location_array in test_result_list:
         pdf.set_font('Courier', 'B', 15)
         pdf.cell(w= 0, h= 10,txt= location_array[1]["location"], border= 'B', ln = 0, align= 'C')
         pdf.ln(10)
         for test in location_array:
             pdf.ln(10)
             for value in test:
                pdf.set_font('Courier', 'B', 12)
                pdf.cell(col_width, th, txt=str(value) +':'+'  ', border=0, align='', )
                pdf.set_font('Courier', '', 10.0)
                pdf.cell(col_width, th, txt=str(test[value]), border=0, align='',)
                pdf.ln(2*th)
             pdf.ln(5)

    # for dic in test_result_list:
    #     pdf.ln(10)
    #     for value in dic:
    #         pdf.set_font('Courier', 'B', 12)
    #         pdf.cell(col_width, th, txt=str(value) +':'+'  ', border=0, align='', )
    #         pdf.set_font('Courier', '', 10.0)
    #         pdf.cell(col_width, th, txt=str(dic[value]), border=0, align='',)
    #         pdf.ln(2*th)
    #     pdf.ln(5)

    # for dic in test_result_list:
    #     cells = pdf.multi_cell(col_width, th, txt="Placeholder text")
    #     index=0
    #     for value in dic:
    #         pdf.set_font('Courier', 'B', 12)
    #         if index >= len(cells):
    #                 break
    #         cell = cells[index]
    #         cell.set_text(cell.get_text() + str(value) + ':')
    #         pdf.set_font('Courier', '', 10.0)
    #         cell.set_text(pdf.cell.get_text() + str(dic[value]) + '\n')
    #         index += 1
    #     pdf.cell(cell)

   

  # creating the pdf in container's file system path - /app/pdfs/test_report.pdf 
    pdf.output(name="/app/pdfs/test_report.pdf",dest= 'f')
    logger.info("created pdf!")

    return upload_pdf(file_path='/app/pdfs/test_report.pdf')

def sort_by_location(data):
    data = [json.d(item) for item in data]
    location_values = set([d['location'] for d in data])
    result = {location: [] for location in location_values}

    for d in data:
        result[d['location']].append(d)
    return result


def on_request(ch, method, props, body):
    if body != None:
        logger.info("sent RPC")
        response = create_pdf_and_upload()
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)


class PDF(FPDF):
    def header(self):
        # Logo
        self.image('Hatal_logo.png', 10, 8, 33)
        # Courier bold 15
        self.set_font('Courier', 'B', 15)
        self.ln(35)


def upload_pdf(file_path):
    logger.info("Uploading file to file hosting service and creating a URL...")
    domain = os.getenv('file-hosting') or "file-hosting"
    url = f'http://{domain}:80/upload?token={os.getenv("TOKEN")}'
    with open(file_path, 'rb') as f:
        files = {'file': ('test_report.pdf', f)}
        response = requests.post(url, files=files)
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            url = f'http://{domain}:80/files/test_report.pdf?token={os.getenv("TOKEN")}'
            logger.info("File uploaded successfully")
            r = requests.get(url)
            if r.ok:
                logger.info("GET request successful")
                logger.info("Sending URL to controller")
                return url
            else:
                logger.error(f"Something went wrong with GET request - {r.status_code}")
        else:
            logger.info("File upload failed.")
            return "File upload failed."
    else:
        logger.error(f"Request failed with status code: {response.status_code}")
        return f"Request failed with status code: {response.status_code}"
