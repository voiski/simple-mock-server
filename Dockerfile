FROM python:2-alpine3.7
LABEL maintainer="alannunesv@gmail.com"

RUN pip install pyaml

EXPOSE 80
ENTRYPOINT [ "simple-mock-server.py","80" ]

COPY . /usr
