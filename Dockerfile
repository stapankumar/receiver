FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY wsgi.py .
COPY .env .
COPY create_schema.py .
COPY init.sql .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 8089

ENTRYPOINT ["./entrypoint.sh"]

