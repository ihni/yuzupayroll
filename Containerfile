FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1        \
    PIP_NO_CACHE_DIR=1

RUN mkdir -p /project/app && \
    mkdir -p /storage/logs &&   \
    chmod -R 777 /storage

WORKDIR /project

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY app/ ./app/

RUN chmod +x main.py

EXPOSE 8000

CMD ["python", "main.py"]