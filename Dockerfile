FROM python:3.8.6

RUN apt-get update
RUN apt-get clean

COPY ./ /usr/local/processor
WORKDIR /usr/local/processor

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

RUN chmod +x ./process.sh
