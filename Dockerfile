FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY honeypot_final.py .

CMD ["python3", "honeypot_final.py"]
