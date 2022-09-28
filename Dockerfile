FROM python:3.10-slim

RUN apt-get update && apt-get install -y git gcc python3-dev

COPY ./ ./
WORKDIR /src

RUN pip install -r requirements.txt
CMD ["python3", "main.py"]