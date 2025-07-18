# Use an official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of flask_app/ into the container
COPY flask_app/ .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
