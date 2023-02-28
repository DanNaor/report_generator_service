FROM python:3.8-slim-buster

LABEL  maintainer="Dan Naor dannaor2001@gmail.com"
LABEL description="A short description of what this image does."
WORKDIR /app
# Install Poetry and dependencies
COPY pyproject.toml .
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Create pdfs directory for storing the pdf
RUN mkdir pdfs

# Copy source code
COPY report_generator_lib.py \
     report_generator.py \
     mongo_handler.py \
     Hatal_logo.png \
     wait \
     /app/

# Set permissions on wait script
RUN chmod +x /app/wait

# Define start command
CMD /app/wait && ./report_generator.py