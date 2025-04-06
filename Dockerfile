# Use an official Python runtime as a parent image
FROM python:3.11.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required by some Python packages
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*
# Add any system dependencies if needed later

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# Respecting the .dockerignore file
COPY . .

# Make port 9000 available to the world outside this container
# EXPOSE 9000

# Run server when the container launches
# CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "9000"] 

# Run python file when the container launches
CMD ["python", "main.py"]