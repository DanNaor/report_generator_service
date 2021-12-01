FROM python:3.8-slim-buster
RUN pip install pika
RUN pip install minio
RUN pip install pymongo
WORKDIR /app
COPY  controller.py . 
COPY  controller_lib.py .
COPY simple_json.json .
CMD ["controller.py"]
ENTRYPOINT ["python"]                            
