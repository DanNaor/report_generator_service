#! /bin/sh
docker-compose up --build -d
docker-compose logs -f -t controller report_generator