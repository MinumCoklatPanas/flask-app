FROM python:3.9-slim-buster

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

EXPOSE 5000

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
