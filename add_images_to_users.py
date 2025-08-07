#!/usr/bin/env python
import os
import sys
import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Portfolio

def download_image(url, filename):
    """Скачивает изображение по URL и возвращает объект File"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Создаем временный файл
        temp_file = NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_file.write(response.content)
        temp_file.flush()
        
        # Создаем объект File
        django_file = File(open(temp_file.name, 'rb'), name=filename)
        return django_file
    except Exception as e:
        print(f"Ошибка при скачивании изображения {url}: {e}")
        return None

def add_images_to_performer():
    """Добавляет изображения к исполнителю"""
    phone = '+77754184629'
    
    try:
        performer = User.objects.get(phone_number=phone)
        print(f"Найден исполнитель: {performer.first_name} {performer.last_name}")
        
        # Добавляем фото профиля, если его нет
        if not performer.profile_photo:
            profile_photo_url = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop"
            profile_photo = download_image(profile_photo_url, f'performer_{phone}_profile.jpg')
            if profile_photo:
                performer.profile_photo.save(f'performer_{phone}_profile.jpg', profile_photo, save=True)
                print(f"✅ Добавлено фото профиля для исполнителя")
        
        # Добавляем портфолио, если его нет
        if not performer.portfolio_set.exists():
            portfolio_urls = [
                "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=400&h=400&fit=crop",
                "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=400&h=400&fit=crop",
                "https://images.unsplash.com/photo-1513151233558-d860c5398176?w=400&h=400&fit=crop",
                "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=400&h=400&fit=crop",
                "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=400&h=400&fit=crop"
            ]
            
            for i, url in enumerate(portfolio_urls, 1):
                portfolio_photo = download_image(url, f'performer_{phone}_portfolio_{i}.jpg')
                if portfolio_photo:
                    Portfolio.objects.create(
                        user=performer,
                        photo=portfolio_photo,
                        description=f'Работа #{i} - Профессиональное мероприятие'
                    )
                    print(f"✅ Добавлено фото портфолио #{i}")
        
        return performer
        
    except User.DoesNotExist:
        print(f"❌ Пользователь с номером {phone} не найден!")
        return None

def add_images_to_customer():
    """Добавляет изображения к заказчику"""
    phone = '+77081619013'
    
    try:
        customer = User.objects.get(phone_number=phone)
        print(f"Найден заказчик: {customer.first_name} {customer.last_name}")
        
        # Добавляем фото профиля, если его нет
        if not customer.profile_photo:
            profile_photo_url = "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop"
            profile_photo = download_image(profile_photo_url, f'customer_{phone}_profile.jpg')
            if profile_photo:
                customer.profile_photo.save(f'customer_{phone}_profile.jpg', profile_photo, save=True)
                print(f"✅ Добавлено фото профиля для заказчика")
        
        return customer
        
    except User.DoesNotExist:
        print(f"❌ Пользователь с номером {phone} не найден!")
        return None

def main():
    print("🖼️ Добавление изображений к пользователям...")
    print("=" * 50)
    
    # Добавляем изображения к исполнителю
    performer = add_images_to_performer()
    print()
    
    # Добавляем изображения к заказчику
    customer = add_images_to_customer()
    print()
    
    print("=" * 50)
    print("✅ Добавление изображений завершено!")

if __name__ == '__main__':
    main() 