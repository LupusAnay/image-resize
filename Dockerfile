FROM python:3.6
WORKDIR /usr/src/app

EXPOSE 5000
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt && \
    groupadd uwsgi && useradd -g uwsgi uwsgi

COPY . /usr/src/app

CMD [ "uwsgi", "--ini", "app.ini"]
