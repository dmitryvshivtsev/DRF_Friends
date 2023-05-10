FROM python:3.10

RUN mkdir -p /usr/src/Django_Friends
COPY . /usr/src/Django_Friends
WORKDIR /usr/src/Django_Friends

ENTRYPOINT ["bash", "./install.sh"]
