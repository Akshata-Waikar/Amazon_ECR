# Dockerfile at root of Amazon_ECR/

FROM python:3.10-slim

WORKDIR /app

# Copy everything from flask_app folder
COPY flask_app/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
