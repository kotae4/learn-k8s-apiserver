# syntax=docker/dockerfile:1
FROM python:3.10-alpine

ENV FASTAPI_LISTEN_PORT=27525
ENV DB_HOST=db.local.testapp.private
ENV DB_PORT=3306
ENV DB_DRIVER=mysql+pymysql
ENV DB_USERNAME=badmin
ENV DB_PASSWORD=vagrant
ENV DB_DATABASE=appdb

EXPOSE $FASTAPI_LISTEN_PORT

WORKDIR /
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /apiserver
ADD learn-k8s-apiserver/ .

WORKDIR /
ENTRYPOINT uvicorn apiserver.main:app --host 0.0.0.0 --port $FASTAPI_LISTEN_PORT --log-config=apiserver/log_conf.yaml --reload --reload-dir apiserver