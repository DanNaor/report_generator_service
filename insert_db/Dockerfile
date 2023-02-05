FROM python:3.8-slim-buster

RUN pip install pika
RUN pip install pymongo

WORKDIR /app

ADD db_insert.py /app
ADD wait /app
ADD mongo_handler.py /app
ADD global_test_config.json /app
#add all files 
COPY simple_json_pass.json simple_json_fail_*.json /app/
RUN chmod +x /app/wait

CMD /app/wait && ./db_insert.py
