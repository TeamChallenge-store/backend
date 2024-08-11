FROM python:3.12.1-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

ADD pyproject.toml /backend/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi --no-dev

COPY . /backend/

CMD sh -c "python manage.py wait_for_db && \
           python manage.py collectstatic --noinput && \
           python manage.py migrate && \
           gunicorn core.config.wsgi:application --bind 0.0.0.0:8000 -w 2"
