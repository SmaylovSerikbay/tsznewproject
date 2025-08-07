#!/usr/bin/env python3
"""
Скрипт для обновления существующего видео
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import Portfolio

def update_video():
    """Обновляет существующее видео"""
    print("🔧 Обновляем существующее видео...")
    
    # Находим видео
    video_item = Portfolio.objects.filter(media_type='video').first()
    
    if video_item:
        print(f"Найдено видео: {video_item.id}")
        print(f"Файл: {video_item.video.name}")
        
        # Обновляем размер файла
        if video_item.video:
            video_path = video_item.video.path
            if os.path.exists(video_path):
                video_item.file_size = os.path.getsize(video_path)
                print(f"Размер файла: {video_item.file_size} байт")
        
        # Сохраняем изменения
        video_item.save()
        print("✅ Видео обновлено!")
    else:
        print("❌ Видео не найдено")

if __name__ == '__main__':
    update_video()
