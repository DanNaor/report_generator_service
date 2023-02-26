FROM python:3.8-slim-buster
RUN apt-get update && apt-get install -y iputils-ping
RUN pip install pika pymongo fpdf requests minio
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
