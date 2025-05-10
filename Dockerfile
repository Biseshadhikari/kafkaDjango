# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . /app/

# Set the environment variable to disable buffering of stdout/stderr
ENV PYTHONUNBUFFERED 1

# Expose the port Daphne will run on (8000 in this case)
EXPOSE 8000

# Run Daphne to serve the application
CMD ["daphne", "project.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
