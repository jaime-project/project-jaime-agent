FROM python:3.9-slim

ARG ARG_VERSION=local

ENV VERSION=${ARG_VERSION}
ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=80
ENV RUN_ON_DOCKER=true
ENV TZ America/Argentina/Buenos_Aires

CMD gunicorn -b ${PYTHON_HOST}:${PYTHON_PORT} --worker-connections 10000 --threads 4 app:app

WORKDIR /home/src

COPY . .
RUN pip install -r requirements.txt --upgrade pip

ADD resources/oc.tar.gz /usr/local/bin/
RUN rm -fr resources