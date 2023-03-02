FROM python:3.8-slim-buster

LABEL  maintainer="Dan Naor dannaor2001@gmail.com"
LABEL description="a micro-service that creates a pdf with the results of the tests"
WORKDIR /app
# Install Poetry and dependencies
COPY pyproject.toml .
COPY poetry.lock .
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Create pdfs directory for storing the pdf
RUN mkdir pdfs

# Copy source code
COPY src \
     assets \
     wait \
     /app/

# Set permissions on wait script
RUN chmod +x /app/wait

# Define start command
CMD /app/wait && ./report_generator.py