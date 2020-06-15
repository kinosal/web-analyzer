FROM python:3.8-slim

COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY app app
COPY manage.py run.py ./

ENV FLASK_APP run.py

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]
