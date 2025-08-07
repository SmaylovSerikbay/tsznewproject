#!/bin/bash

# Подключение к серверу и настройка статических файлов
ssh root@77.246.247.137 << 'EOF'

# Остановить текущий сервер
pkill -f "manage.py runserver"

# Перейти в директорию проекта
cd /var/www/tsz25

# Активировать виртуальное окружение
source venv/bin/activate

# Добавить настройки для статических файлов
echo "DEBUG = True" >> tsz2/settings.py
echo "ALLOWED_HOSTS = ['*']" >> tsz2/settings.py

# Пересобрать статические файлы
python manage.py collectstatic --noinput --clear

# Запустить сервер на порту 80
nohup python manage.py runserver 0.0.0.0:80 > /var/log/tsz25.log 2>&1 &

echo "Сервер запущен на порту 80"
echo "URL: http://77.246.247.137"

EOF 