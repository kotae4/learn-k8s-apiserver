# syntax=docker/dockerfile:1
FROM python:3.10-alpine

ENV FASTAPI_LISTEN_PORT=27525

EXPOSE $FASTAPI_LISTEN_PORT

WORKDIR /
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /apiserver
ADD . .

WORKDIR /
ENTRYPOINT uvicorn apiserver.main:app --host 0.0.0.0 --port $FASTAPI_LISTEN_PORT --log-config=apiserver/log_conf.yaml --reload --reload-dir apiserver