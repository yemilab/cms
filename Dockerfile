FROM python:3.7
LABEL maintainer="code@hyounggyu.com"

RUN apt-get update && \
    apt-get install -y postgresql-client

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn psycopg2-binary

COPY . /code/
WORKDIR /code/

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 8000
ENTRYPOINT ["/code/docker-entrypoint.sh"]
