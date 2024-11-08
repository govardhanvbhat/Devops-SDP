# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install flask mysql.connector

# Copy the rest of the application code into the container
COPY . /app

EXPOSE 5001

# Specify the default command to run the application
CMD ["python", "app.py"]