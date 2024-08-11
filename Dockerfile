FROM python:3.11.4-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apt-get update

# install dependencies
RUN pip install --upgrade pip
RUN pip install django dj-database-url python-dotenv langchain langchain_core langchain_cohere psycopg2-binary whitenoise gunicorn

COPY . /app

ENTRYPOINT [ "gunicorn", "scheduler.wsgi", "-b", "0.0.0.0:8000"]