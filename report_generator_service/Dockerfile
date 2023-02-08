FROM python:3.8-slim-buster
RUN pip install pika
RUN pip install minio
RUN pip install pymongo
RUN pip install fpdf
RUN pip install requests
WORKDIR /app
RUN mkdir pdfs
ADD report_generator_lib.py /app 
ADD report_generator.py /app
ADD mongo_handler.py /app
ADD Hatal_logo.png /app
ADD toker_is_a_baddy.png /app
ADD wait /app
RUN chmod +x /app/wait
CMD /app/wait && ./report_generator.py