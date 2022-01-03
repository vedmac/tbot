FROM python:3.9.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY /. .

RUN pip install poetry \
    && poetry config virtualenvs.create false && poetry install --no-dev

CMD poetry run main 