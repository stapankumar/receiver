FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
COPY parser ./parser
COPY db ./db
COPY .env .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
