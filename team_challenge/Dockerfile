FROM python:3.12.1-alpine

# Оновлення pip
RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY . /backend
WORKDIR /backend

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install && rm -rf $POETRY_CACHE_DIR

ENV VIRTUAL_ENV=/backend/.venv \
    PATH="/backend/.venv/bin:$PATH"

COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]
