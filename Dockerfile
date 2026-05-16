FROM python:3.9-slim

RUN apt-get update && \
    apt-get -y install tesseract-ocr tesseract-ocr-ita

RUN apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--workers", "4", "--threads", "6", "--timeout", "120", "--graceful-timeout", "30", "--bind", "0.0.0.0:5000", "app:app"]