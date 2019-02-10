FROM python:3.6
WORKDIR /usr/src/backend

EXPOSE 5000
COPY ./requirements.txt /usr/src/backend/requirements.txt

RUN pip install -r requirements.txt && \
    groupadd uwsgi && useradd -g uwsgi uwsgi && \
    mkdir images

COPY . /usr/src/backend


CMD [ "uwsgi", "--ini", "app.ini"]
