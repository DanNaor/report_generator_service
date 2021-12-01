FROM python:3.8-slim-buster
RUN pip install pika
RUN pip install minio
RUN pip install pymongo
WORKDIR /app
COPY  controller.py . 
CMD ["controller.py"]
ENTRYPOINT ["python"]                            
