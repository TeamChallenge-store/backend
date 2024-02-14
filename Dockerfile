# Використовуємо базовий образ Python версії 3.12.1
FROM python:3.12.1

# Оновлюємо pip
RUN pip install --upgrade pip

# Встановлюємо залежності за допомогою pip
COPY requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir -r /backend/requirements.txt

# Копіюємо ключ автентифікації Google у контейнер
COPY team_challenge/teamchallenge-2105a95396e0.json /backend/teamchallenge-2105a95396e0.json

# Встановлюємо змінну середовища для шляху до ключа автентифікації Google
ENV GOOGLE_APPLICATION_CREDENTIALS=/backend/teamchallenge-2105a95396e0.json

# Встановлюємо змінні середовища для уникнення створення байткоду та безбуферного виводу Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копіюємо всі файли з поточної директорії у контейнер у директорію /backend
COPY . /backend

# Встановлюємо робочу директорію у /backend
WORKDIR /backend

# Запускаємо Gunicorn для обробки веб-запитів
CMD ["gunicorn", "team_challenge.wsgi:application", "--bind", "0.0.0.0:8000"]
