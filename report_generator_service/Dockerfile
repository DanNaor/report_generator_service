FROM python:3.8-slim-buster
RUN pip install pika
RUN pip install minio
RUN pip install pymongo
WORKDIR /app
COPY report_generator_lib.py .
COPY  report_generator.py . 
CMD ["report_generator.py"]
ENTRYPOINT ["python"]                            
