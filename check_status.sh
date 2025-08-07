#!/bin/bash

echo "🔍 Проверка статуса проекта на сервере..."

# Проверяем подключение к серверу
echo "📡 Подключение к серверу..."
ssh root@77.246.247.137 << 'EOF'
    echo "✅ Подключение успешно"
    
    # Проверяем Docker
    echo "🐳 Проверяем Docker..."
    docker --version
    docker-compose --version
    
    # Проверяем статус контейнеров
    echo "📊 Статус контейнеров:"
    cd /root/tsznewproject 2>/dev/null && docker-compose ps || echo "❌ Проект не найден"
    
    # Проверяем логи
    echo "📝 Последние логи web контейнера:"
    cd /root/tsznewproject 2>/dev/null && docker-compose logs web --tail=5 2>/dev/null || echo "❌ Логи недоступны"
    
    # Проверяем доступность сервисов
    echo "🌐 Проверка доступности:"
    curl -I http://localhost:80 2>/dev/null | head -1 || echo "❌ Nginx недоступен"
    curl -I http://localhost:8000 2>/dev/null | head -1 || echo "❌ Django недоступен"
    
    echo "✅ Проверка завершена"
EOF

echo "🎉 Скрипт выполнен"
