#!/usr/bin/env python3
"""
Скрипт для импорта данных на сервер
"""

import os
import sys
import django
import json
from PIL import Image, ImageOps
import io

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import City, ServiceType, User, Portfolio
from django.contrib.auth.hashers import make_password
from django.core.files import File

def fix_image_orientation(image_path):
    """Исправляет ориентацию изображения согласно EXIF"""
    try:
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        
        # Конвертируем в RGB если нужно
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Сохраняем исправленное изображение
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)
        
        return output
    except Exception as e:
        print(f"Ошибка при исправлении ориентации {image_path}: {e}")
        return None

def import_data():
    """Импортирует данные из JSON файлов"""
    print("🚀 Начинаем импорт данных...")
    
    # Импорт городов
    print("\n📍 Импортируем города...")
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            cities_data = json.load(f)
        
        for city_data in cities_data:
            city, created = City.objects.get_or_create(
                name=city_data['name'],
                defaults={
                    'is_active': city_data.get('is_active', True),
                    'created_at': city_data.get('created_at')
                }
            )
            if created:
                print(f"  ✅ Создан город: {city.name}")
            else:
                print(f"  ⚠️ Город уже существует: {city.name}")
    except FileNotFoundError:
        print("  ❌ Файл cities.json не найден")
    
    # Импорт типов услуг
    print("\n🔧 Импортируем типы услуг...")
    try:
        with open('service_types.json', 'r', encoding='utf-8') as f:
            service_types_data = json.load(f)
        
        for service_data in service_types_data:
            service, created = ServiceType.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'is_active': service_data.get('is_active', True),
                    'created_at': service_data.get('created_at')
                }
            )
            if created:
                print(f"  ✅ Создан тип услуги: {service.name}")
            else:
                print(f"  ⚠️ Тип услуги уже существует: {service.name}")
    except FileNotFoundError:
        print("  ❌ Файл service_types.json не найден")
    
    # Импорт пользователей
    print("\n👥 Импортируем пользователей...")
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data.get('email', ''),
                    'first_name': user_data.get('first_name', ''),
                    'last_name': user_data.get('last_name', ''),
                    'phone': user_data.get('phone', ''),
                    'user_type': user_data.get('user_type', 'customer'),
                    'is_active': user_data.get('is_active', True),
                    'is_staff': user_data.get('is_staff', False),
                    'is_superuser': user_data.get('is_superuser', False),
                    'date_joined': user_data.get('date_joined'),
                    'last_login': user_data.get('last_login')
                }
            )
            
            # Устанавливаем пароль
            if created:
                user.password = make_password(user_data.get('password', 'password123'))
                user.save()
                print(f"  ✅ Создан пользователь: {user.username}")
            else:
                print(f"  ⚠️ Пользователь уже существует: {user.username}")
    except FileNotFoundError:
        print("  ❌ Файл users.json не найден")
    
    # Импорт портфолио
    print("\n🖼️ Импортируем портфолио...")
    try:
        with open('portfolio.json', 'r', encoding='utf-8') as f:
            portfolio_data = json.load(f)
        
        for item_data in portfolio_data:
            try:
                user = User.objects.get(username=item_data['user'])
                
                # Проверяем, существует ли уже такой элемент портфолио
                existing_item = Portfolio.objects.filter(
                    user=user,
                    media_type=item_data.get('media_type', 'image')
                ).first()
                
                if existing_item:
                    print(f"  ⚠️ Портфолио уже существует для пользователя: {user.username}")
                    continue
                
                portfolio = Portfolio.objects.create(
                    user=user,
                    media_type=item_data.get('media_type', 'image'),
                    title=item_data.get('title', ''),
                    description=item_data.get('description', ''),
                    created_at=item_data.get('created_at')
                )
                
                # Обрабатываем файл
                if item_data.get('media_type') == 'video':
                    video_path = f"media/{item_data['video']}"
                    if os.path.exists(video_path):
                        with open(video_path, 'rb') as f:
                            portfolio.video.save(os.path.basename(video_path), File(f), save=False)
                        print(f"  ✅ Добавлено видео для: {user.username}")
                else:
                    image_path = f"media/{item_data['image']}"
                    if os.path.exists(image_path):
                        # Исправляем ориентацию изображения
                        fixed_image = fix_image_orientation(image_path)
                        if fixed_image:
                            portfolio.image.save(os.path.basename(image_path), File(fixed_image), save=False)
                            print(f"  ✅ Добавлено изображение (с исправленной ориентацией) для: {user.username}")
                        else:
                            # Если не удалось исправить, загружаем как есть
                            with open(image_path, 'rb') as f:
                                portfolio.image.save(os.path.basename(image_path), File(f), save=False)
                            print(f"  ✅ Добавлено изображение для: {user.username}")
                
                portfolio.save()
                
            except User.DoesNotExist:
                print(f"  ❌ Пользователь не найден: {item_data['user']}")
            except Exception as e:
                print(f"  ❌ Ошибка при импорте портфолио: {e}")
                
    except FileNotFoundError:
        print("  ❌ Файл portfolio.json не найден")
    
    print("\n✅ Импорт завершен!")

if __name__ == '__main__':
    import_data()
