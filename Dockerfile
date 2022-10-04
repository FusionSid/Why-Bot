FROM python:3.10-slim

RUN apt-get update && apt-get install -y git gcc python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /
COPY ./ ./
WORKDIR /src

RUN pip install -r requirements.txt --no-cache-dir
CMD ["python3", "main.py"]