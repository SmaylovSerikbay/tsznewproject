#!/bin/bash

# Скрипт для деплоя проекта на сервер
# Использование: ./deploy_to_server.sh

SERVER_IP="77.246.247.137"
SERVER_USER="root"
GITHUB_REPO="https://github.com/SmaylovSerikbay/tsznewproject"
PROJECT_NAME="tsznewproject"

echo "🚀 Начинаем деплой проекта на сервер $SERVER_IP..."

# 1. Очистка сервера
echo "🧹 Очистка сервера..."
ssh $SERVER_USER@$SERVER_IP << 'EOF'
    echo "Останавливаем все Docker контейнеры..."
    docker stop $(docker ps -aq) 2>/dev/null || true
    docker rm $(docker ps -aq) 2>/dev/null || true
    
    echo "Удаляем все Docker образы..."
    docker rmi $(docker images -q) 2>/dev/null || true
    
    echo "Удаляем все Docker volumes..."
    docker volume rm $(docker volume ls -q) 2>/dev/null || true
    
    echo "Удаляем все Docker networks..."
    docker network prune -f
    
    echo "Очищаем систему..."
    apt-get update
    apt-get autoremove -y
    apt-get autoclean
    
    echo "Очищаем временные файлы..."
    rm -rf /tmp/*
    rm -rf /var/tmp/*
    
    echo "Очищаем старые проекты..."
    rm -rf /root/tsz30
    rm -rf /root/tsznewproject
    rm -rf /var/www/*
    
    echo "✅ Сервер очищен"
EOF

# 2. Установка Docker и Docker Compose
echo "🐳 Установка Docker и Docker Compose..."
ssh $SERVER_USER@$SERVER_IP << 'EOF'
    echo "Удаляем старые версии Docker..."
    apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
    
    echo "Устанавливаем зависимости..."
    apt-get update
    apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        git \
        unzip
    
    echo "Добавляем официальный GPG ключ Docker..."
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    echo "Добавляем репозиторий Docker..."
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    echo "Устанавливаем Docker..."
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io
    
    echo "Запускаем Docker..."
    systemctl start docker
    systemctl enable docker
    
    echo "Устанавливаем Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    echo "✅ Docker и Docker Compose установлены"
EOF

# 3. Клонирование проекта
echo "📥 Клонирование проекта с GitHub..."
ssh $SERVER_USER@$SERVER_IP << EOF
    echo "Клонируем репозиторий..."
    git clone $GITHUB_REPO /root/$PROJECT_NAME
    cd /root/$PROJECT_NAME
    
    echo "Проверяем структуру проекта..."
    ls -la
    
    echo "✅ Проект склонирован"
EOF

# 4. Настройка переменных окружения
echo "⚙️ Настройка переменных окружения..."
ssh $SERVER_USER@$SERVER_IP << 'EOF'
    cd /root/tsznewproject
    
    echo "Создаем .env файл..."
    cat > .env << 'ENVFILE'
# Django settings
DEBUG=False
SECRET_KEY=tsz30-production-secret-key-2025-change-this-in-production
ALLOWED_HOSTS=77.246.247.137,localhost,127.0.0.1

# Database settings
DATABASE_URL=postgres://tsz30_user:tsz30_password@db:5432/tsz30_db

# Static and media files
STATIC_URL=/static/
MEDIA_URL=/media/

# Security settings
CSRF_TRUSTED_ORIGINS=http://77.246.247.137,http://localhost
ENVFILE
    
    echo "✅ Переменные окружения настроены"
EOF

# 5. Запуск проекта
echo "🚀 Запуск проекта..."
ssh $SERVER_USER@$SERVER_IP << 'EOF'
    cd /root/tsznewproject
    
    echo "Собираем и запускаем Docker контейнеры..."
    docker-compose up -d --build
    
    echo "Ждем запуска базы данных..."
    sleep 30
    
    echo "Выполняем миграции..."
    docker-compose exec -T web python manage.py migrate
    
    echo "Создаем суперпользователя..."
    docker-compose exec -T web python manage.py createsuperuser --noinput --username admin --email admin@example.com || true
    
    echo "Собираем статические файлы..."
    docker-compose exec -T web python manage.py collectstatic --noinput
    
    echo "✅ Проект запущен"
EOF

# 6. Проверка статуса
echo "🔍 Проверка статуса..."
ssh $SERVER_USER@$SERVER_IP << 'EOF'
    echo "Статус Docker контейнеров:"
    docker-compose -f /root/tsznewproject/docker-compose.yml ps
    
    echo "Логи веб-сервера:"
    docker-compose -f /root/tsznewproject/docker-compose.yml logs web --tail=10
    
    echo "Проверка доступности сервисов:"
    curl -I http://localhost:80 || echo "Nginx недоступен"
    curl -I http://localhost:8000 || echo "Django недоступен"
    
    echo "Информация о системе:"
    df -h
    free -h
    docker system df
EOF

echo "🎉 Деплой завершен!"
echo "🌐 Сайт доступен по адресу: http://77.246.247.137"
echo "📊 Мониторинг: docker-compose -f /root/tsznewproject/docker-compose.yml logs -f"
