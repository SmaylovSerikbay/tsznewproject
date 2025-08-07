#!/usr/bin/env python
"""
Скрипт для миграции данных из SQLite в PostgreSQL
Сохраняет все данные включая фотографии исполнителей
"""

import os
import sys
import django
import json
import shutil
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, City, ServiceType, Portfolio, Order

def backup_sqlite_data():
    """Создает резервную копию SQLite базы данных"""
    print("💾 Создание резервной копии SQLite базы данных...")
    
    if os.path.exists('db.sqlite3'):
        backup_name = f'db.sqlite3.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        shutil.copy2('db.sqlite3', backup_name)
        print(f"✅ Резервная копия создана: {backup_name}")

def export_data_to_json():
    """Экспортирует данные из Django моделей в JSON файлы"""
    print("📤 Экспорт данных в JSON...")
    
    # Экспорт городов
    cities_data = []
    for city in City.objects.all():
        city_data = {
            'name': city.name,
            'is_active': city.is_active,
            'created_at': city.created_at.isoformat() if city.created_at else None
        }
        cities_data.append(city_data)
    
    with open('cities_export.json', 'w', encoding='utf-8') as f:
        json.dump(cities_data, f, ensure_ascii=False, indent=2)
    
    # Экспорт типов услуг
    service_types_data = []
    for service_type in ServiceType.objects.all():
        service_type_data = {
            'code': service_type.code,
            'name': service_type.name,
            'description': service_type.description,
            'icon': service_type.icon,
            'is_active': service_type.is_active,
            'sort_order': service_type.sort_order,
            'created_at': service_type.created_at.isoformat() if service_type.created_at else None
        }
        service_types_data.append(service_type_data)
    
    with open('service_types_export.json', 'w', encoding='utf-8') as f:
        json.dump(service_types_data, f, ensure_ascii=False, indent=2)
    
    # Экспорт пользователей
    users_data = []
    for user in User.objects.all():
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'user_type': user.user_type,
            'is_phone_verified': user.is_phone_verified,
            'rating': user.rating,
            'company_name': user.company_name,
            'bio': user.bio,
            'services': user.services,
            'email_notifications': user.email_notifications,
            'whatsapp_notifications': user.whatsapp_notifications,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'date_joined': user.date_joined.isoformat() if user.date_joined else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }
        
        # Сохраняем фото профиля
        if user.profile_photo:
            photo_path = user.profile_photo.path
            if os.path.exists(photo_path):
                photo_filename = f"profile_photos/{user.username}_{os.path.basename(photo_path)}"
                shutil.copy2(photo_path, f"media_backup/{photo_filename}")
                user_data['profile_photo'] = photo_filename
        
        # Сохраняем связь с городом
        if user.city:
            user_data['city_name'] = user.city.name
        
        # Сохраняем связь с типом услуги
        if user.service_type:
            user_data['service_type_code'] = user.service_type.code
        
        users_data.append(user_data)
    
    with open('users_export.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    # Экспорт портфолио
    portfolio_data = []
    for portfolio in Portfolio.objects.all():
        portfolio_item = {
            'user_username': portfolio.user.username,
            'created_at': portfolio.created_at.isoformat() if portfolio.created_at else None
        }
        
        # Сохраняем изображение портфолио
        if portfolio.image:
            image_path = portfolio.image.path
            if os.path.exists(image_path):
                image_filename = f"portfolio/{portfolio.user.username}_{os.path.basename(image_path)}"
                shutil.copy2(image_path, f"media_backup/{image_filename}")
                portfolio_item['image'] = image_filename
        
        portfolio_data.append(portfolio_item)
    
    with open('portfolio_export.json', 'w', encoding='utf-8') as f:
        json.dump(portfolio_data, f, ensure_ascii=False, indent=2)
    
    # Экспорт заказов
    orders_data = []
    for order in Order.objects.all():
        order_data = {
            'customer_username': order.customer.username,
            'performer_username': order.performer.username if order.performer else None,
            'title': order.title,
            'event_type': order.event_type,
            'event_date': order.event_date.isoformat() if order.event_date else None,
            'city': order.city,
            'venue': order.venue,
            'guest_count': order.guest_count,
            'description': order.description,
            'budget': str(order.budget),
            'services': order.services,
            'selected_performers': order.selected_performers,
            'status': order.status,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'updated_at': order.updated_at.isoformat() if order.updated_at else None,
            'details': order.details,
            'order_type': order.order_type
        }
        
        if order.tariff:
            order_data['tariff_name'] = order.tariff.name
        
        orders_data.append(order_data)
    
    with open('orders_export.json', 'w', encoding='utf-8') as f:
        json.dump(orders_data, f, ensure_ascii=False, indent=2)
    
    print("✅ Данные экспортированы в JSON файлы")

def create_media_backup():
    """Создает резервную копию медиа файлов"""
    print("📁 Создание резервной копии медиа файлов...")
    
    if os.path.exists('media'):
        if os.path.exists('media_backup'):
            shutil.rmtree('media_backup')
        shutil.copytree('media', 'media_backup')
        print("✅ Резервная копия медиа файлов создана: media_backup/")

def main():
    """Основная функция миграции"""
    print("🚀 Начинаем миграцию данных из SQLite в PostgreSQL...")
    
    # Создаем резервные копии
    backup_sqlite_data()
    create_media_backup()
    
    # Экспортируем данные
    export_data_to_json()
    
    print("\n📋 Следующие шаги:")
    print("1. Запустите PostgreSQL и Django с новыми настройками")
    print("2. Выполните миграции: python manage.py migrate")
    print("3. Запустите скрипт импорта: python import_to_postgres.py")
    print("\n📁 Созданные файлы:")
    print("- db.sqlite3.backup (резервная копия SQLite)")
    print("- media_backup/ (резервная копия медиа файлов)")
    print("- *_export.json (экспортированные данные)")

if __name__ == '__main__':
    main()
