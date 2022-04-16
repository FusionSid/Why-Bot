FROM python:3.9-slim

RUN apt-get update && apt-get upgrade && apt-get -y install gcc python3-dev

RUN apt-get install -y git

COPY ./requirements.txt .
COPY ./src ./src
COPY .env .env 

RUN pip install -r requirements.txt

WORKDIR /src
CMD ["python3", "main.py"]