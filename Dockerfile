FROM python:3.8.5-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/

RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        postgresql-dev \
    && pip install --upgrade pip setuptools wheel pipenv==2018.11.26 \
    && pipenv install --dev --system --deploy \
    && rm -rf /root/.cache/pip