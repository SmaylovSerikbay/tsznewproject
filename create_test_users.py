#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Portfolio, Tariff, BusyDate, Category

def create_test_users():
    print("Создание тестовых пользователей...")
    
    # Создаем заказчика
    customer = User.objects.create_user(
        username='customer_test',
        email='customer@test.com',
        password='test123456',
        first_name='Алексей',
        last_name='Петров',
        phone_number='+77771234567',
        city='Алматы',
        user_type='customer',
        is_phone_verified=True
    )
    print(f"✅ Создан заказчик: {customer.get_full_name()}")
    
    # Создаем исполнителя-фотографа
    photographer = User.objects.create_user(
        username='photographer_test',
        email='photographer@test.com',
        password='test123456',
        first_name='Мария',
        last_name='Иванова',
        phone_number='+77776543210',
        city='Алматы',
        user_type='performer',
        service_type='photo',
        company_name='Фотостудия "Момент"',
        bio='Профессиональный фотограф с 5-летним опытом. Специализируюсь на свадебной и портретной фотографии. Создаю красивые и запоминающиеся кадры для ваших особенных моментов.',
        is_phone_verified=True,
        rating=4.8
    )
    print(f"✅ Создан фотограф: {photographer.get_full_name()}")
    
    # Создаем исполнителя-ведущего
    host = User.objects.create_user(
        username='host_test',
        email='host@test.com',
        password='test123456',
        first_name='Дмитрий',
        last_name='Сидоров',
        phone_number='+77779876543',
        city='Астана',
        user_type='performer',
        service_type='host',
        company_name='Ведущий Дмитрий',
        bio='Опытный ведущий мероприятий. Проведу ваше торжество на высшем уровне с юмором и энтузиазмом. Создам незабываемую атмосферу для ваших гостей.',
        is_phone_verified=True,
        rating=4.9
    )
    print(f"✅ Создан ведущий: {host.get_full_name()}")
    
    # Создаем исполнителя-музыканта
    musician = User.objects.create_user(
        username='musician_test',
        email='musician@test.com',
        password='test123456',
        first_name='Анна',
        last_name='Козлова',
        phone_number='+77774567890',
        city='Алматы',
        user_type='performer',
        service_type='music',
        company_name='Музыкальная группа "Мелодия"',
        bio='Живая музыка для ваших мероприятий. Классика, джаз, поп-музыка. Создаем особую атмосферу с помощью профессионального исполнения.',
        is_phone_verified=True,
        rating=4.7
    )
    print(f"✅ Создан музыкант: {musician.get_full_name()}")
    
    # Создаем тарифы для фотографа
    tariff1 = Tariff.objects.create(
        user=photographer,
        name='Базовый пакет',
        price=Decimal('50000'),
        description='2 часа съемки, 50 обработанных фото, онлайн-галерея'
    )
    
    tariff2 = Tariff.objects.create(
        user=photographer,
        name='Стандартный пакет',
        price=Decimal('80000'),
        description='4 часа съемки, 100 обработанных фото, печать 20 фото, онлайн-галерея'
    )
    
    tariff3 = Tariff.objects.create(
        user=photographer,
        name='Премиум пакет',
        price=Decimal('120000'),
        description='6 часов съемки, 200 обработанных фото, печать 50 фото, фотоальбом, онлайн-галерея'
    )
    print(f"✅ Созданы тарифы для фотографа: {tariff1.name}, {tariff2.name}, {tariff3.name}")
    
    # Создаем тарифы для ведущего
    tariff4 = Tariff.objects.create(
        user=host,
        name='Базовое ведение',
        price=Decimal('40000'),
        description='Ведение мероприятия до 4 часов, музыкальное сопровождение'
    )
    
    tariff5 = Tariff.objects.create(
        user=host,
        name='Полный пакет',
        price=Decimal('60000'),
        description='Ведение мероприятия до 6 часов, музыкальное сопровождение, конкурсы и игры'
    )
    print(f"✅ Созданы тарифы для ведущего: {tariff4.name}, {tariff5.name}")
    
    # Создаем тарифы для музыканта
    tariff6 = Tariff.objects.create(
        user=musician,
        name='Дуэт',
        price=Decimal('35000'),
        description='2 музыканта, 2 часа выступления'
    )
    
    tariff7 = Tariff.objects.create(
        user=musician,
        name='Квартет',
        price=Decimal('60000'),
        description='4 музыканта, 3 часа выступления'
    )
    print(f"✅ Созданы тарифы для музыканта: {tariff6.name}, {tariff7.name}")
    
    # Создаем занятые даты для исполнителей
    today = date.today()
    
    # Занятые даты для фотографа
    busy_dates_photographer = [
        today + timedelta(days=7),   # Через неделю
        today + timedelta(days=14),  # Через 2 недели
        today + timedelta(days=21),  # Через 3 недели
    ]
    
    for busy_date in busy_dates_photographer:
        BusyDate.objects.create(user=photographer, date=busy_date)
    print(f"✅ Созданы занятые даты для фотографа: {len(busy_dates_photographer)} дат")
    
    # Занятые даты для ведущего
    busy_dates_host = [
        today + timedelta(days=10),  # Через 10 дней
        today + timedelta(days=17),  # Через 17 дней
    ]
    
    for busy_date in busy_dates_host:
        BusyDate.objects.create(user=host, date=busy_date)
    print(f"✅ Созданы занятые даты для ведущего: {len(busy_dates_host)} дат")
    
    # Занятые даты для музыканта
    busy_dates_musician = [
        today + timedelta(days=5),   # Через 5 дней
        today + timedelta(days=12),  # Через 12 дней
        today + timedelta(days=19),  # Через 19 дней
    ]
    
    for busy_date in busy_dates_musician:
        BusyDate.objects.create(user=musician, date=busy_date)
    print(f"✅ Созданы занятые даты для музыканта: {len(busy_dates_musician)} дат")
    
    print("\n" + "="*50)
    print("🎉 ТЕСТОВЫЕ АККАУНТЫ СОЗДАНЫ УСПЕШНО!")
    print("="*50)
    print("\n📋 ДАННЫЕ ДЛЯ ВХОДА:")
    print("\n👤 ЗАКАЗЧИК:")
    print(f"   Логин: customer_test")
    print(f"   Email: customer@test.com")
    print(f"   Пароль: test123456")
    print(f"   Телефон: +77771234567")
    
    print("\n📸 ФОТОГРАФ:")
    print(f"   Логин: photographer_test")
    print(f"   Email: photographer@test.com")
    print(f"   Пароль: test123456")
    print(f"   Телефон: +77776543210")
    print(f"   Компания: Фотостудия 'Момент'")
    print(f"   Рейтинг: 4.8")
    
    print("\n🎤 ВЕДУЩИЙ:")
    print(f"   Логин: host_test")
    print(f"   Email: host@test.com")
    print(f"   Пароль: test123456")
    print(f"   Телефон: +77779876543")
    print(f"   Компания: Ведущий Дмитрий")
    print(f"   Рейтинг: 4.9")
    
    print("\n🎵 МУЗЫКАНТ:")
    print(f"   Логин: musician_test")
    print(f"   Email: musician@test.com")
    print(f"   Пароль: test123456")
    print(f"   Телефон: +77774567890")
    print(f"   Компания: Музыкальная группа 'Мелодия'")
    print(f"   Рейтинг: 4.7")
    
    print("\n💰 СОЗДАННЫЕ ТАРИФЫ:")
    print(f"   Фотограф: 3 тарифа (50,000 - 120,000 тенге)")
    print(f"   Ведущий: 2 тарифа (40,000 - 60,000 тенге)")
    print(f"   Музыкант: 2 тарифа (35,000 - 60,000 тенге)")
    
    print("\n📅 ЗАНЯТЫЕ ДАТЫ:")
    print(f"   Фотограф: {len(busy_dates_photographer)} дат")
    print(f"   Ведущий: {len(busy_dates_host)} дат")
    print(f"   Музыкант: {len(busy_dates_musician)} дат")
    
    print("\n🌐 ССЫЛКА НА САЙТ:")
    print("   http://localhost:8000")
    
    print("\n" + "="*50)

if __name__ == '__main__':
    create_test_users() 