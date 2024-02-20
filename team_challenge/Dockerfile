FROM python:3.12.1-alpine

RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /venv

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY . /backend

WORKDIR /backend
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev \
    && pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
