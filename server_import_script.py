#!/usr/bin/env python3
import os
import sys
import django
import json
import shutil
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
os.environ['DATABASE_URL'] = 'postgres://tsz30_user:tsz30_password@db:5432/tsz30_db'
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = 'toisozvezdoi.kz,www.toisozvezdoi.kz,77.246.247.137,localhost,127.0.0.1'

django.setup()

from main.models import User, City, ServiceType, Portfolio, Order
from django.contrib.auth.hashers import make_password

def import_cities():
    """Импортирует города"""
    print("🏙️ Импортируем города...")
    with open('migration_data/cities_export.json', 'r', encoding='utf-8') as f:
        cities_data = json.load(f)
    
    for city_data in cities_data:
        city, created = City.objects.get_or_create(
            name=city_data['name'],
            defaults={
                'is_active': city_data.get('is_active', True),
                'created_at': datetime.fromisoformat(city_data['created_at'].replace('Z', '+00:00')) if city_data.get('created_at') else None
            }
        )
        if created:
            print(f"✅ Создан город: {city.name}")

def import_service_types():
    """Импортирует типы услуг"""
    print("🔧 Импортируем типы услуг...")
    with open('migration_data/service_types_export.json', 'r', encoding='utf-8') as f:
        service_types_data = json.load(f)
    
    for service_type_data in service_types_data:
        service_type, created = ServiceType.objects.get_or_create(
            code=service_type_data['code'],
            defaults={
                'name': service_type_data['name'],
                'description': service_type_data.get('description', ''),
                'icon': service_type_data.get('icon', ''),
                'is_active': service_type_data.get('is_active', True),
                'sort_order': service_type_data.get('sort_order', 0),
                'created_at': datetime.fromisoformat(service_type_data['created_at'].replace('Z', '+00:00')) if service_type_data.get('created_at') else None
            }
        )
        if created:
            print(f"✅ Создан тип услуги: {service_type.name}")

def import_users():
    """Импортирует пользователей"""
    print("👥 Импортируем пользователей...")
    with open('migration_data/users_export.json', 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    for user_data in users_data:
        # Получаем связанные объекты
        city = None
        if user_data.get('city_name'):
            try:
                city = City.objects.get(name=user_data['city_name'])
            except City.DoesNotExist:
                print(f"⚠️ Город не найден: {user_data['city_name']}")
        
        service_type = None
        if user_data.get('service_type_code'):
            try:
                service_type = ServiceType.objects.get(code=user_data['service_type_code'])
            except ServiceType.DoesNotExist:
                print(f"⚠️ Тип услуги не найден: {user_data['service_type_code']}")
        
        # Создаем пользователя
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data.get('email', ''),
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
                'phone_number': user_data.get('phone_number'),
                'user_type': user_data.get('user_type', 'customer'),
                'is_phone_verified': user_data.get('is_phone_verified', False),
                'rating': user_data.get('rating', 0.0),
                'company_name': user_data.get('company_name'),
                'bio': user_data.get('bio', ''),
                'services': user_data.get('services', []),
                'email_notifications': user_data.get('email_notifications', True),
                'whatsapp_notifications': user_data.get('whatsapp_notifications', True),
                'is_staff': user_data.get('is_staff', False),
                'is_superuser': user_data.get('is_superuser', False),
                'is_active': user_data.get('is_active', True),
                'city': city,
                'service_type': service_type,
                'password': make_password('default_password_123')  # Временный пароль
            }
        )
        
        if created:
            print(f"✅ Создан пользователь: {user.username}")
            
            # Копируем фото профиля
            if user_data.get('profile_photo'):
                source_path = f"media_backup/{user_data['profile_photo']}"
                if os.path.exists(source_path):
                    dest_path = f"media/{user_data['profile_photo']}"
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(source_path, dest_path)
                    user.profile_photo = user_data['profile_photo']
                    user.save()
                    print(f"📸 Фото профиля скопировано для {user.username}")

def import_portfolio():
    """Импортирует портфолио"""
    print("🖼️ Импортируем портфолио...")
    with open('migration_data/portfolio_export.json', 'r', encoding='utf-8') as f:
        portfolio_data = json.load(f)
    
    for portfolio_item in portfolio_data:
        try:
            user = User.objects.get(username=portfolio_item['user_username'])
            
            # Копируем изображение
            if portfolio_item.get('image'):
                source_path = f"media_backup/{portfolio_item['image']}"
                if os.path.exists(source_path):
                    dest_path = f"media/{portfolio_item['image']}"
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(source_path, dest_path)
                    
                    # Создаем запись в портфолио
                    portfolio, created = Portfolio.objects.get_or_create(
                        user=user,
                        image=portfolio_item['image'],
                        defaults={
                            'created_at': datetime.fromisoformat(portfolio_item['created_at'].replace('Z', '+00:00')) if portfolio_item.get('created_at') else None
                        }
                    )
                    if created:
                        print(f"✅ Создано портфолио для {user.username}")
        except User.DoesNotExist:
            print(f"⚠️ Пользователь не найден: {portfolio_item['user_username']}")

def main():
    """Основная функция импорта"""
    print("🚀 Начинаем импорт данных в PostgreSQL...")
    
    # Импортируем данные в правильном порядке
    import_cities()
    import_service_types()
    import_users()
    import_portfolio()
    
    print("✅ Импорт завершен!")
    print("📋 Следующие шаги:")
    print("1. Проверьте данные в админке Django")
    print("2. Измените пароли пользователей")
    print("3. Проверьте работу сайта")

if __name__ == '__main__':
    main()
