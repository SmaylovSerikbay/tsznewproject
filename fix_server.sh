#!/bin/bash

echo "🔧 Полное исправление сервера..."

# Останавливаем контейнеры
echo "📦 Останавливаем контейнеры..."
docker-compose down

# Удаляем старые статические файлы
echo "🗑️ Удаляем старые статические файлы..."
sudo rm -rf staticfiles/

# Удаляем старые volumes (если нужно)
echo "🗑️ Удаляем старые volumes..."
docker volume rm tsznewproject_static_files tsznewproject_media_files 2>/dev/null || true

# Пересобираем образ
echo "🔨 Пересобираем Docker образ..."
docker-compose build --no-cache

# Запускаем контейнеры
echo "🚀 Запускаем контейнеры..."
docker-compose up -d

# Ждем запуска
echo "⏳ Ждем запуска контейнеров..."
sleep 30

# Проверяем статус
echo "🔍 Проверяем статус контейнеров..."
docker-compose ps

# Проверяем логи
echo "📋 Проверяем логи web контейнера..."
docker-compose logs web

echo "✅ Исправление сервера завершено!"
