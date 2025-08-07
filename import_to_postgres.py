#!/usr/bin/env python
"""
Скрипт для импорта данных в PostgreSQL
Импортирует данные из JSON файлов и восстанавливает медиа файлы
"""

import os
import sys
import django
import json
from datetime import datetime
from decimal import Decimal
import shutil

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import *
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def import_cities():
    """Импортирует города"""
    print("🏙️ Импорт городов...")
    
    if not os.path.exists('cities_export.json'):
        print("⚠️ Файл cities_export.json не найден")
        return
    
    with open('cities_export.json', 'r', encoding='utf-8') as f:
        cities_data = json.load(f)
    
    for city_data in cities_data:
        city, created = City.objects.get_or_create(
            name=city_data['name'],
            defaults={
                'is_active': city_data.get('is_active', True),
                'created_at': datetime.fromisoformat(city_data['created_at']) if city_data.get('created_at') else None
            }
        )
        if created:
            print(f"✅ Создан город: {city.name}")
        else:
            print(f"ℹ️ Город уже существует: {city.name}")

def import_service_types():
    """Импортирует типы услуг"""
    print("🔧 Импорт типов услуг...")
    
    if not os.path.exists('service_types_export.json'):
        print("⚠️ Файл service_types_export.json не найден")
        return
    
    with open('service_types_export.json', 'r', encoding='utf-8') as f:
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
                'created_at': datetime.fromisoformat(service_type_data['created_at']) if service_type_data.get('created_at') else None
            }
        )
        if created:
            print(f"✅ Создан тип услуги: {service_type.name}")
        else:
            print(f"ℹ️ Тип услуги уже существует: {service_type.name}")

def import_users():
    """Импортирует пользователей"""
    print("👥 Импорт пользователей...")
    
    if not os.path.exists('users_export.json'):
        print("⚠️ Файл users_export.json не найден")
        return
    
    with open('users_export.json', 'r', encoding='utf-8') as f:
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
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
                'email': user_data.get('email', ''),
                'user_type': user_data['user_type'],
                'phone_number': user_data.get('phone_number'),
                'is_phone_verified': user_data.get('is_phone_verified', False),
                'rating': user_data.get('rating', 0),
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
                'date_joined': datetime.fromisoformat(user_data['date_joined']) if user_data.get('date_joined') else None,
                'last_login': datetime.fromisoformat(user_data['last_login']) if user_data.get('last_login') else None,
            }
        )
        
        if created:
            print(f"✅ Создан пользователь: {user.username}")
            
            # Восстанавливаем профильное фото
            if user_data.get('profile_photo'):
                photo_path = f"media_backup/{user_data['profile_photo']}"
                if os.path.exists(photo_path):
                    try:
                        with open(photo_path, 'rb') as f:
                            user.profile_photo.save(
                                os.path.basename(photo_path),
                                File(f),
                                save=True
                            )
                        print(f"📸 Восстановлено фото профиля для: {user.username}")
                    except Exception as e:
                        print(f"❌ Ошибка восстановления фото для {user.username}: {e}")
        else:
            print(f"ℹ️ Пользователь уже существует: {user.username}")

def import_portfolio():
    """Импортирует портфолио"""
    print("🖼️ Импорт портфолио...")
    
    if not os.path.exists('portfolio_export.json'):
        print("⚠️ Файл portfolio_export.json не найден")
        return
    
    with open('portfolio_export.json', 'r', encoding='utf-8') as f:
        portfolio_data = json.load(f)
    
    for portfolio_item in portfolio_data:
        try:
            user = User.objects.get(username=portfolio_item['user_username'])
            
            portfolio, created = Portfolio.objects.get_or_create(
                user=user,
                created_at=datetime.fromisoformat(portfolio_item['created_at']) if portfolio_item.get('created_at') else None
            )
            
            if created:
                print(f"✅ Создана запись портфолио для: {user.username}")
                
                # Восстанавливаем изображение
                if portfolio_item.get('image'):
                    image_path = f"media_backup/{portfolio_item['image']}"
                    if os.path.exists(image_path):
                        try:
                            with open(image_path, 'rb') as f:
                                portfolio.image.save(
                                    os.path.basename(image_path),
                                    File(f),
                                    save=True
                                )
                            print(f"🖼️ Восстановлено изображение портфолио для: {user.username}")
                        except Exception as e:
                            print(f"❌ Ошибка восстановления изображения для {user.username}: {e}")
            else:
                print(f"ℹ️ Портфолио уже существует для: {user.username}")
                
        except User.DoesNotExist:
            print(f"⚠️ Пользователь не найден: {portfolio_item['user_username']}")

def import_orders():
    """Импортирует заказы"""
    print("📋 Импорт заказов...")
    
    if not os.path.exists('orders_export.json'):
        print("⚠️ Файл orders_export.json не найден")
        return
    
    with open('orders_export.json', 'r', encoding='utf-8') as f:
        orders_data = json.load(f)
    
    for order_data in orders_data:
        try:
            customer = User.objects.get(username=order_data['customer_username'])
            performer = None
            if order_data.get('performer_username'):
                try:
                    performer = User.objects.get(username=order_data['performer_username'])
                except User.DoesNotExist:
                    print(f"⚠️ Исполнитель не найден: {order_data['performer_username']}")
            
            tariff = None
            if order_data.get('tariff_name'):
                try:
                    tariff = Tariff.objects.get(name=order_data['tariff_name'])
                except Tariff.DoesNotExist:
                    print(f"⚠️ Тариф не найден: {order_data['tariff_name']}")
            
            order, created = Order.objects.get_or_create(
                customer=customer,
                title=order_data['title'],
                event_date=datetime.fromisoformat(order_data['event_date']).date() if order_data.get('event_date') else None,
                defaults={
                    'performer': performer,
                    'event_type': order_data['event_type'],
                    'city': order_data['city'],
                    'venue': order_data.get('venue', ''),
                    'guest_count': order_data['guest_count'],
                    'description': order_data.get('description', ''),
                    'budget': Decimal(order_data['budget']) if order_data.get('budget') else Decimal('0'),
                    'services': order_data.get('services', []),
                    'selected_performers': order_data.get('selected_performers', {}),
                    'status': order_data['status'],
                    'created_at': datetime.fromisoformat(order_data['created_at']) if order_data.get('created_at') else None,
                    'updated_at': datetime.fromisoformat(order_data['updated_at']) if order_data.get('updated_at') else None,
                    'details': order_data.get('details', ''),
                    'order_type': order_data.get('order_type', 'request'),
                    'tariff': tariff
                }
            )
            
            if created:
                print(f"✅ Создан заказ: {order.title}")
            else:
                print(f"ℹ️ Заказ уже существует: {order.title}")
                
        except User.DoesNotExist:
            print(f"⚠️ Заказчик не найден: {order_data['customer_username']}")

def restore_media_files():
    """Восстанавливает медиа файлы"""
    print("📁 Восстановление медиа файлов...")
    
    if os.path.exists('media_backup'):
        if os.path.exists('media'):
            shutil.rmtree('media')
        shutil.copytree('media_backup', 'media')
        print("✅ Медиа файлы восстановлены")
    else:
        print("⚠️ Папка media_backup не найдена")

def main():
    """Основная функция импорта"""
    print("🚀 Начинаем импорт данных в PostgreSQL...")
    
    # Импортируем данные в правильном порядке
    import_cities()
    import_service_types()
    import_users()
    import_portfolio()
    import_orders()
    
    # Восстанавливаем медиа файлы
    restore_media_files()
    
    print("\n✅ Импорт завершен!")
    print("📊 Статистика:")
    print(f"- Города: {City.objects.count()}")
    print(f"- Типы услуг: {ServiceType.objects.count()}")
    print(f"- Пользователи: {User.objects.count()}")
    print(f"- Портфолио: {Portfolio.objects.count()}")
    print(f"- Заказы: {Order.objects.count()}")

if __name__ == '__main__':
    main()
