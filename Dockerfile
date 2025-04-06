# Stage 1: Builder stage
FROM python:3.11.11-slim AS Build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the application code (respecting .dockerignore)
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.11-alpine

# Copy the application code from the builder stage
COPY --from=build /app /app

# Make port 9000 available to the world outside this container
# EXPOSE 9000

# Run server when the container launches
# CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "9000"] 

# Run python file when the container launches
CMD ["python", "main.py"]