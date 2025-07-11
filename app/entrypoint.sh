#!/bin/sh

set -e

# Ожидаем зависимости
python manage.py wait_for_db --timeout=30
python manage.py wait_for_redis --timeout=30

# Применяем миграции
python manage.py makemigrations --no-input
python manage.py migrate --no-input

# Проверяем состояние миграций
python manage.py check_migrations

# Собираем статику
python manage.py collectstatic --noinput --clear

# Запускаем основной процесс
exec "$@"
