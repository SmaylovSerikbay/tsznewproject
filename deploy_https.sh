#!/bin/bash

echo "🚀 Начинаем деплой с HTTPS..."

# Остановка и удаление старых контейнеров
echo "📦 Останавливаем старые контейнеры..."
docker-compose down

# Получение SSL сертификата (если нужно)
echo "🔒 Проверяем SSL сертификат..."
if [ ! -f "/etc/letsencrypt/live/toisozvezdoi.kz/fullchain.pem" ]; then
    echo "📜 Получаем SSL сертификат..."
    certbot certonly --standalone -d toisozvezdoi.kz -d www.toisozvezdoi.kz --non-interactive --agree-tos --email admin@toisozvezdoi.kz
else
    echo "✅ SSL сертификат уже существует"
fi

# Запуск контейнеров
echo "🐳 Запускаем контейнеры..."
docker-compose up -d

# Ожидание запуска
echo "⏳ Ждем запуска контейнеров..."
sleep 30

# Проверка статуса
echo "🔍 Проверяем статус контейнеров..."
docker-compose ps

# Проверка доступности
echo "🌐 Проверяем доступность сайта..."
echo "HTTP (должен редиректить на HTTPS):"
curl -I http://toisozvezdoi.kz

echo "HTTPS:"
curl -I https://toisozvezdoi.kz

echo "✅ Деплой завершен!"
echo "🌍 Сайт доступен по адресу: https://toisozvezdoi.kz"
