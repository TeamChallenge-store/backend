# Використовуємо офіційний образ Node.js як базовий образ
FROM node:18-alpine

# Встановлюємо робочу директорію в контейнері
WORKDIR /client

# Копіюємо файли package.json та package-lock.json до контейнера
COPY package.json package-lock.json ./

# Встановлюємо залежності проекту
RUN npm install

# Копіюємо усі інші файли проекту до контейнера
COPY . /client

# Запускаємо збірку React додатку з Vite
RUN npx vite build

# Вказуємо порт, на якому буде прослуховувати сервер
EXPOSE 4173

# Запускаємо застосунок з хостом 0.0.0.0
CMD ["npx", "vite", "preview", "--host", "0.0.0.0"]
