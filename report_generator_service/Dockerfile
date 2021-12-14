FROM python:3.8-slim-buster
RUN pip install pika
RUN pip install minio
RUN pip install pymongo
RUN pip install pandas
WORKDIR /app
ADD report_generator_lib.py /app 
ADD report_generator.py /app
RUN chmod +x /app/report_generator.py
RUN chmod +x /app/report_generator_lib.py
ADD wait /app
RUN chmod +x /app/wait
CMD /app/wait && ./report_generator.py
# CMD ["report_generator.py"]
# ENTRYPOINT ["python"]                            