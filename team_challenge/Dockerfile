# Використовуємо базовий образ Python версії 3.12.1
FROM python:3.12.1-alpine

# Оновлюємо pip
RUN pip install --upgrade pip

# Встановлюємо змінні середовища для уникнення створення байткоду та безбуферного виводу Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Створюємо нову директорію для віртуального середовища
RUN mkdir /venv

# Створюємо та активуємо віртуальне середовище
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Копіюємо файли проекту в контейнер
COPY . /backend

# Встановлюємо залежності за допомогою pip
WORKDIR /backend
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev \
    && pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
