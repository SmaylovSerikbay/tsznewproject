#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Portfolio, Tariff, BusyDate

def create_user_accounts():
    print("Создание пользовательских аккаунтов...")
    
    # Создаем исполнителя с номером +77085446945
    performer = User.objects.create_user(
        username='performer_user',
        email='performer@example.com',
        password='user123456',
        first_name='Алихан',
        last_name='Нурланов',
        phone_number='+77085446945',
        city='Алматы',
        user_type='performer',
        service_type='photo',  # Фотограф
        company_name='Фотостудия "Алихан"',
        bio='Профессиональный фотограф с опытом более 3 лет. Специализируюсь на свадебной, портретной и коммерческой фотографии. Создаю качественные и запоминающиеся кадры для ваших особенных моментов.',
        is_phone_verified=True,
        rating=4.6
    )
    print(f"✅ Создан исполнитель: {performer.get_full_name()} ({performer.phone_number})")
    
    # Создаем заказчика с номером +77776875411
    customer = User.objects.create_user(
        username='customer_user',
        email='customer@example.com',
        password='user123456',
        first_name='Данияр',
        last_name='Ахметов',
        phone_number='+77776875411',
        city='Астана',
        user_type='customer',
        is_phone_verified=True
    )
    print(f"✅ Создан заказчик: {customer.get_full_name()} ({customer.phone_number})")
    
    # Создаем тарифы для исполнителя
    tariff1 = Tariff.objects.create(
        user=performer,
        name='Базовый пакет',
        price=Decimal('45000'),
        description='2 часа съемки, 40 обработанных фото, онлайн-галерея'
    )
    
    tariff2 = Tariff.objects.create(
        user=performer,
        name='Стандартный пакет',
        price=Decimal('75000'),
        description='4 часа съемки, 80 обработанных фото, печать 15 фото, онлайн-галерея'
    )
    
    tariff3 = Tariff.objects.create(
        user=performer,
        name='Премиум пакет',
        price=Decimal('110000'),
        description='6 часов съемки, 150 обработанных фото, печать 30 фото, фотоальбом, онлайн-галерея'
    )
    print(f"✅ Созданы тарифы для исполнителя: {tariff1.name}, {tariff2.name}, {tariff3.name}")
    
    # Создаем занятые даты для исполнителя
    today = date.today()
    busy_dates = [
        today + timedelta(days=3),   # Через 3 дня
        today + timedelta(days=8),   # Через неделю
        today + timedelta(days=15),  # Через 2 недели
        today + timedelta(days=22),  # Через 3 недели
    ]
    
    for busy_date in busy_dates:
        BusyDate.objects.create(user=performer, date=busy_date)
    print(f"✅ Созданы занятые даты для исполнителя: {len(busy_dates)} дат")
    
    print("\n" + "="*50)
    print("🎉 ПОЛЬЗОВАТЕЛЬСКИЕ АККАУНТЫ СОЗДАНЫ!")
    print("="*50)
    print("\n📋 ДАННЫЕ ДЛЯ ВХОДА:")
    
    print("\n📸 ИСПОЛНИТЕЛЬ (Фотограф):")
    print(f"   Логин: performer_user")
    print(f"   Email: performer@example.com")
    print(f"   Пароль: user123456")
    print(f"   Телефон: +77085446945")
    print(f"   Имя: Алихан Нурланов")
    print(f"   Компания: Фотостудия 'Алихан'")
    print(f"   Город: Алматы")
    print(f"   Рейтинг: 4.6")
    print(f"   Тарифы: 3 (45,000 - 110,000 ₸)")
    
    print("\n👤 ЗАКАЗЧИК:")
    print(f"   Логин: customer_user")
    print(f"   Email: customer@example.com")
    print(f"   Пароль: user123456")
    print(f"   Телефон: +77776875411")
    print(f"   Имя: Данияр Ахметов")
    print(f"   Город: Астана")
    
    print("\n📅 ЗАНЯТЫЕ ДАТЫ ИСПОЛНИТЕЛЯ:")
    for i, busy_date in enumerate(busy_dates, 1):
        print(f"   {i}. {busy_date.strftime('%d.%m.%Y')}")
    
    print("\n🌐 ССЫЛКА НА САЙТ:")
    print("   http://localhost:8000")
    
    print("\n" + "="*50)

if __name__ == '__main__':
    create_user_accounts() 