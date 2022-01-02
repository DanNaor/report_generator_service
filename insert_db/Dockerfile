FROM python:3.8-slim-buster
RUN pip install pika
RUN pip install pymongo
WORKDIR /app
ADD db_insert.py /app 
ADD simple_json.json /app
ADD global_test_config.json /app
ADD wait /app
ADD mongo_handler.py /app
RUN chmod +x /app/wait
CMD /app/wait && ./db_insert.py
# CMD ["controller.py"]
# ENTRYPOINT ["python"]                            