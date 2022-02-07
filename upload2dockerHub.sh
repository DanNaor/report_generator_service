#! /bin/sh
docker build -t  dannaor/report_generator:0.0.2 ./report_generator_service
docker push dannaor/report_generator:0.0.2