FROM python:3.8.10-slim-buster

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get --fix-missing update && apt-get --fix-broken install 

RUN python3 -m pip install --upgrade pip && apt install -y postgresql postgresql-contrib     

RUN pip install -r requirements.txt 