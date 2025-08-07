#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Order, City, ServiceType

def add_test_orders():
    """Добавляет тестовые доступные заявки для исполнителей"""
    
    # Получаем города и типы услуг
    cities = list(City.objects.filter(is_active=True))
    service_types = list(ServiceType.objects.filter(is_active=True))
    
    if not cities:
        print("❌ Нет активных городов в базе данных")
        return
    
    if not service_types:
        print("❌ Нет активных типов услуг в базе данных")
        return
    
    # Получаем или создаем тестового заказчика
    customer, created = User.objects.get_or_create(
        phone_number='+77771234567',
        defaults={
            'username': 'test_customer',
            'first_name': 'Тестовый',
            'last_name': 'Заказчик',
            'email': 'test_customer@example.com',
            'user_type': 'customer',
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Создан тестовый заказчик: {customer.get_full_name()}")
    else:
        print(f"✅ Используется существующий заказчик: {customer.get_full_name()}")
    
    # Удаляем старые тестовые заявки
    old_orders = Order.objects.filter(customer=customer, title__startswith='Тестовая заявка')
    if old_orders.exists():
        old_orders.delete()
        print("🗑️ Удалены старые тестовые заявки")
    
    # Создаем новые тестовые заявки
    event_types = ['wedding', 'birthday', 'corporate', 'anniversary', 'graduation', 'party']
    event_titles = [
        'Свадьба в стиле "Винтаж"',
        'День рождения ребенка',
        'Корпоративный ужин',
        'Юбилей бабушки',
        'Выпускной вечер',
        'Вечеринка в честь повышения',
        'Романтический ужин',
        'Празднование покупки квартиры',
        'День рождения мамы',
        'Корпоративная вечеринка',
        'Свадьба в морском стиле',
        'Детский праздник',
        'Встреча выпускников',
        'Празднование годовщины',
        'День рождения папы'
    ]
    
    venues = [
        'Ресторан "Золотой"',
        'Кафе "Уютное"',
        'Банкетный зал "Престиж"',
        'Ресторан "Морской"',
        'Кафе "Солнечное"',
        'Банкетный зал "Элит"',
        'Ресторан "Старый город"',
        'Кафе "Весна"',
        'Банкетный зал "Люкс"',
        'Ресторан "Панорама"'
    ]
    
    orders_created = 0
    
    for i in range(20):  # Создаем 20 тестовых заявок
        # Случайная дата в ближайшие 3 месяца
        days_from_now = random.randint(1, 90)
        event_date = datetime.now().date() + timedelta(days=days_from_now)
        
        # Случайный тип мероприятия
        event_type = random.choice(event_types)
        
        # Случайный город
        city = random.choice(cities)
        
        # Случайный тип услуги
        service_type = random.choice(service_types)
        
        # Случайный бюджет
        budget_min = Decimal(random.randint(20000, 100000))
        budget_max = budget_min + Decimal(random.randint(10000, 50000))
        
        # Создаем заявку
        order = Order.objects.create(
            customer=customer,
            title=f"Тестовая заявка #{i+1}: {random.choice(event_titles)}",
            event_type=event_type,
            event_date=event_date,
            venue=random.choice(venues),
            guest_count=random.randint(10, 150),
            description=f"Тестовая заявка для проверки функциональности. Мероприятие: {event_type}. Требуется профессиональный исполнитель для качественного проведения мероприятия.",
            budget_min=budget_min,
            budget_max=budget_max,
            city=city.name,
            services=[service_type.code],
            status='new',
            order_type='request'
        )
        
        orders_created += 1
        print(f"✅ Создана заявка: {order.title} ({city.name}, {service_type.name})")
    
    print(f"\n🎉 Успешно создано {orders_created} тестовых заявок!")
    print(f"📊 Статистика:")
    print(f"   - Заказчик: {customer.get_full_name()}")
    print(f"   - Города: {', '.join(set([order.city for order in Order.objects.filter(customer=customer, title__startswith='Тестовая заявка')]))}")
    print(f"   - Типы услуг: {', '.join(set([service_type.name for service_type in service_types]))}")
    print(f"   - Бюджет: от {min([order.budget_min for order in Order.objects.filter(customer=customer, title__startswith='Тестовая заявка')])} до {max([order.budget_max for order in Order.objects.filter(customer=customer, title__startswith='Тестовая заявка')])} ₸")

if __name__ == '__main__':
    print("🚀 Добавление тестовых доступных заявок...")
    add_test_orders()
    print("✅ Готово!") 