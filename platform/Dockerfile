# Python base image
FROM python:3.6

# Updating repository sources
RUN apt-get update

WORKDIR /app
COPY . /app

# Copying requirements.txt file
COPY requirements.txt requirements.txt

# pip install
RUN pip install --no-cache -r requirements.txt

# Exposing ports
EXPOSE 8888

# Launch server app
ENTRYPOINT python ./server.py
