# Use an official Python runtime as a parent image
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run server.py when the container launches
CMD ["python", "server.py"]
