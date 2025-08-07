#!/usr/bin/env python3
"""
Скрипт для проверки данных портфолио
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import Portfolio, User

def check_portfolio():
    """Проверяет данные портфолио"""
    print("🔍 Проверяем данные портфолио...")
    
    # Получаем все элементы портфолио
    portfolio_items = Portfolio.objects.all()
    print(f"📊 Всего элементов портфолио: {portfolio_items.count()}")
    
    for item in portfolio_items:
        print(f"\n--- Элемент ID: {item.id} ---")
        print(f"Пользователь: {item.user.username}")
        print(f"Тип медиа: {item.media_type}")
        print(f"Название: '{item.title}'")
        print(f"Описание: '{item.description}'")
        
        if item.media_type == 'video':
            print(f"Видео файл: {item.video.name if item.video else 'НЕТ'}")
            print(f"Превью: {item.thumbnail.name if item.thumbnail else 'НЕТ'}")
            print(f"Длительность: {item.duration}")
            print(f"Размер файла: {item.file_size}")
            
            # Проверяем, существует ли файл
            if item.video:
                video_path = item.video.path
                print(f"Путь к видео: {video_path}")
                print(f"Файл существует: {os.path.exists(video_path)}")
        else:
            print(f"Изображение: {item.image.name if item.image else 'НЕТ'}")
            
            # Проверяем, существует ли файл
            if item.image:
                image_path = item.image.path
                print(f"Путь к изображению: {image_path}")
                print(f"Файл существует: {os.path.exists(image_path)}")
        
        print(f"Дата создания: {item.created_at}")

if __name__ == '__main__':
    check_portfolio()
