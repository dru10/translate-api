FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --only main

WORKDIR /app/src

COPY src/ .

WORKDIR /app
