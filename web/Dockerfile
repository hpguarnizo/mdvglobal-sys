FROM codi0/python:latest

ARG DJANGO_ENV

ENV PYTHONUNBUFFERED=1
ENV WEB_DIR=/web

RUN mkdir $WEB_DIR

WORKDIR $WEB_DIR

ADD requirements/base.txt $WEB_DIR/  
ADD requirements/$DJANGO_ENV.txt $WEB_DIR/

RUN pip3 install -r $DJANGO_ENV.txt

ADD . $WEB_DIR/  
