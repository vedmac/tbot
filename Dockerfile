FROM python:3.9.5-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY /. .

RUN apt update -y \
	&& apt-get autoremove -y && apt-get autoclean -y \
    && pip install poetry \
    && poetry config virtualenvs.create false && poetry install --no-dev

CMD poetry run main 