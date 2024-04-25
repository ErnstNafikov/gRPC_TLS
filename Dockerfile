FROM python:3

ENV PYTHONUNBUFFERED 1

COPY /client /grpc_server/client
COPY /server /grpc_server/server
COPY /protos /grpc_server/protos
COPY requirements.txt /grpc_server
WORKDIR /grpc_server

RUN \
 python3 -m pip install --root-user-action=ignore -r requirements.txt --no-cache-dir
 
 CMD python -m server 0.0.0.0:5000