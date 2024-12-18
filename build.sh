#!/bin/bash

# Собираем Docker образы
echo "Собираем Docker образы..."
docker-compose build

# Запускаем контейнеры в фоновом режиме
echo "Запускаем контейнеры..."
docker-compose up -d

# Ожидаем несколько секунд, чтобы база данных успела подняться
echo "Ожидаем запуск базы данных..."
sleep 10  # Можно увеличить время ожидания, если необходимо

# Проверяем, что база данных доступна
echo "Проверяем доступность базы данных..."
until docker-compose exec db pg_isready -U admin -d fuses_db; do
  echo "Ожидаем готовности базы данных..."
  sleep 2
done

# Проводим миграции базы данных
echo "Проводим миграции базы данных..."
docker-compose exec web flask db upgrade  # Здесь предполагается, что вы используете миграции с Flask-Migrate

# Проверяем, что приложение Flask работает
echo "Проверяем, что приложение Flask работает..."
docker-compose exec web flask --version

echo "Проект собран и готов к использованию!"
