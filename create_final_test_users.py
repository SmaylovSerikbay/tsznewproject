#!/usr/bin/env python
import os
import sys
import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from io import BytesIO

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Portfolio
from django.contrib.auth.hashers import make_password

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

def create_performer_user():
    """Создает аккаунт исполнителя"""
    phone = '+77754184629'
    
    # Проверяем, существует ли уже пользователь с таким номером
    if User.objects.filter(phone_number=phone).exists():
        print(f"Пользователь с номером {phone} уже существует!")
        return User.objects.get(phone_number=phone)
    
    # Создаем пользователя-исполнителя
    performer = User.objects.create(
        phone_number=phone,
        username='miras_performer',
        email='miras.abildin@bk.ru',
        first_name='Мирас',
        last_name='Абильдин',
        city='Астана',
        company_name='TSZ Events',
        service_type='host',
        bio='Профессиональный ведущий мероприятий с 10-летним опытом. Специализируюсь на свадьбах, корпоративах и детских праздниках. Создаю незабываемую атмосферу для каждого мероприятия!',
        user_type='performer',
        is_active=True,
        password=make_password('30031986m')
    )
    
    print(f"✅ Создан исполнитель: {performer.first_name} {performer.last_name}")
    
    # Скачиваем и устанавливаем фото профиля
    profile_photo_url = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face"
    profile_photo = download_image(profile_photo_url, f'performer_{phone}_profile.jpg')
    if profile_photo:
        performer.profile_photo.save(f'performer_{phone}_profile.jpg', profile_photo, save=True)
        print(f"✅ Установлено фото профиля для исполнителя")
    
    # Создаем портфолио (5 изображений)
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

def create_customer_user():
    """Создает аккаунт заказчика"""
    phone = '+77081619013'
    
    # Проверяем, существует ли уже пользователь с таким номером
    if User.objects.filter(phone_number=phone).exists():
        print(f"Пользователь с номером {phone} уже существует!")
        return User.objects.get(phone_number=phone)
    
    # Создаем пользователя-заказчика
    customer = User.objects.create(
        phone_number=phone,
        username='galya_customer',
        email='galya.customer@example.com',
        first_name='Галия',
        last_name='Муханбет',
        city='Астана',
        company_name='',
        service_type='',
        bio='Ищу профессиональных исполнителей для организации качественных мероприятий.',
        user_type='customer',
        is_active=True,
        password=make_password('123456')
    )
    
    print(f"✅ Создан заказчик: {customer.first_name} {customer.last_name}")
    
    # Скачиваем и устанавливаем фото профиля
    profile_photo_url = "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face"
    profile_photo = download_image(profile_photo_url, f'customer_{phone}_profile.jpg')
    if profile_photo:
        customer.profile_photo.save(f'customer_{phone}_profile.jpg', profile_photo, save=True)
        print(f"✅ Установлено фото профиля для заказчика")
    
    return customer

def main():
    print("🎭 Создание финальных тестовых аккаунтов...")
    print("=" * 50)
    
    # Создаем исполнителя
    performer = create_performer_user()
    print()
    
    # Создаем заказчика
    customer = create_customer_user()
    print()
    
    print("=" * 50)
    print("✅ Создание аккаунтов завершено!")
    print()
    print("📱 Данные для входа:")
    print(f"Исполнитель: {performer.phone_number} / 30031986m")
    print(f"Заказчик: {customer.phone_number} / 123456")
    print()
    print("🔗 Ссылки для входа:")
    print(f"http://127.0.0.1:8000/auth/")
    print(f"https://toisozvezdoi.kz/auth/")

if __name__ == '__main__':
    main() 