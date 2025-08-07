#!/usr/bin/env python
import os
import sys
import django
import requests
from django.core.files.base import ContentFile
from pathlib import Path

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

def create_missing_images():
    print("Создание недостающих статических изображений...")
    
    # Создаем директории если их нет
    static_dir = Path('static/images')
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Список недостающих изображений и их URL
    missing_images = {
        'hero-bg.jpg': 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200&h=600&fit=crop',
        'default-avatar.jpg': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&crop=face',
        'default-avatar.png': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&crop=face'
    }
    
    for filename, url in missing_images.items():
        file_path = static_dir / filename
        
        if not file_path.exists():
            try:
                print(f"Загрузка {filename}...")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Создан файл: {filename}")
                
            except Exception as e:
                print(f"❌ Ошибка загрузки {filename}: {e}")
        else:
            print(f"✅ Файл уже существует: {filename}")
    
    print("\n" + "="*50)
    print("🎉 НЕДОСТАЮЩИЕ ИЗОБРАЖЕНИЯ СОЗДАНЫ!")
    print("="*50)
    
    # Проверяем созданные файлы
    print(f"\n📁 Созданные файлы:")
    for filename in missing_images.keys():
        file_path = static_dir / filename
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"   {filename} ({size} байт)")
        else:
            print(f"   {filename} (НЕ СОЗДАН)")

if __name__ == '__main__':
    create_missing_images() 