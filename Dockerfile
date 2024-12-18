# Используем официальный Python runtime как родительский образ
FROM python:3.11-slim

# Устанавливаем зависимости для PostgreSQL и другие утилиты
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем текущую директорию в контейнер
COPY . /app

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт, на котором будет работать Flask
EXPOSE 5000

# Устанавливаем переменные окружения для Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Команда запуска Flask с проверкой доступности БД
CMD ["bash", "-c", "until pg_isready -h db -p 5432 -U admin; do echo 'Waiting for database...'; sleep 2; done && flask run"]
