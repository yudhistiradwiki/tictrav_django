FROM python:3.10-slim-buster

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc libpq-dev && \
    apt clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel

RUN pip install --no-cache-dir \
    -r requirements.txt


COPY . .

CMD gunicorn pa_tictrav.wsgi:application --bind 0.0.0.0:$PORT