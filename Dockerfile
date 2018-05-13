FROM ubuntu:16.04
MAINTAINER Mikhail Volynov

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3

ADD . $WORK

EXPOSE 80

WORKDIR $WORK/src

CMD python3 -u server.py
