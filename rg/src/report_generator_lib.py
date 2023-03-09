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




    # Create a new page for displaying the tests
    pdf.add_page()

    # Move the text cursor to the center of the page
    pdf.cell(80)

    # Set the font and display the title "Tests"
    pdf.set_font('Courier', 'B', 15)
    pdf.cell(30, 10, 'Tests:', 1, 0, 'C')

    # Add a new line for spacing
    pdf.ln(10)

    # Set the font and iterate through the list of test results
    pdf.set_font('Courier', '', 10.0)
    i = 0
    for i, location_array in enumerate(test_result_list):
        
        # Set the font to bold and display the location of the tests
        pdf.set_font('Courier', 'B', 15)
        pdf.cell(w=0, h=10, txt=location_array[1]["location"], border='B', ln=0, align='C')
        pdf.ln(10)
        
        # Set the font to normal and display each test's information on separate lines
        pdf.set_font('Courier', '', 12)
        for test in location_array:
            pdf.ln(10)
            cell_text = ""
            for key, value in test.items():
                cell_text += f"{key}: {value}" + "\n"       
            pdf.multi_cell(0, th*2, txt=cell_text, border=0, align='L')
            pdf.ln(5)
        
        # If this is the last set of tests, add a new page for the next set of tests
        if is_last(test_result_list, i):
            pdf.add_page()

    pdf.add_page()
    # setting the font to Courier, bold, and size 15
    pdf.set_font('Courier', 'B', 15)
    # adding a cell with a border and center alignment containing the title "statistics"
    pdf.cell(0, th*2, 'statistics:', 1, 0, 'C')
    # moving to a new line
    pdf.ln(10)
    # getting statistics from the test_result_list using the get_stats function
    stats=get_stats(test_results=test_result_list)
    # adding a cell with the amount of failed tests using the "num_fail" key in the stats dictionary
    pdf.cell(0,th*2,txt="amount of failed tests- "+str(stats["num_fail"]),ln=10,align='L')
    # adding a cell with the amount of passed tests using the "num_pass" key in the stats dictionary
    pdf.cell(0,th*2,txt="amount of passed tests- "+str(stats["num_pass"]),ln=10,align='L')
    # adding a cell with the amount of types (unique locations) using the length of the "unique_locations" list in the stats dictionary
    pdf.cell(0,th*2,txt="amount of types- "+str(len(stats["unique_locations"])),ln=10,align='L')
    # adding a multi-cell with the types of tests using the "unique_locations" list in the stats dictionary, with a line break between each value
    pdf.multi_cell(0,th*2,txt="types of test-\n"+"\n".join(stats['unique_locations']))

    # creating the pdf in container's file system path - /app/pdfs/test_report.pdf 
    pdf.output(name="/app/pdfs/test_report.pdf",dest= 'f')
    
    logger.info("created pdf!")
    # returning the uploaded pdf file
    return upload_pdf(file_path='/app/pdfs/test_report.pdf')

def is_last(test_result_list, i):
    return i<len(test_result_list)-1

def get_stats(test_results):
    # Initialize counters
    num_fail = 0
    num_pass = 0
    unique_locations = set()

    # Iterate over the documents and update counters and set of unique locations
    for location_array in test_results:
        for document in location_array:
            if document.get("result") == "Fail":
                num_fail += 1
            elif document.get("result") == "Pass":
                num_pass += 1

            unique_locations.add(str(document.get("location")))

    # Return the counters and set of unique locations
    return {"num_fail": num_fail, "num_pass": num_pass, "unique_locations": unique_locations}

    



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
