# Python base image 3.6
FROM python:3.6

# Updating repository sources
RUN apt-get update

COPY . /app
WORKDIR /app

# Copying requirements.txt file
COPY requirements.txt requirements.txt

# pip install
RUN pip install --no-cache -r requirements.txt

# expose port
EXPOSE 5000

# Launch server app
ENTRYPOINT ["python"]
CMD ["server.py"]
