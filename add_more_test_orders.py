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

def add_more_test_orders():
    """Добавляет дополнительные тестовые заявки для большего разнообразия"""
    
    # Получаем города и типы услуг
    cities = list(City.objects.filter(is_active=True))
    service_types = list(ServiceType.objects.filter(is_active=True))
    
    if not cities:
        print("❌ Нет активных городов в базе данных")
        return
    
    if not service_types:
        print("❌ Нет активных типов услуг в базе данных")
        return
    
    # Создаем несколько тестовых заказчиков для разнообразия
    customers_data = [
        {
            'phone': '+77771111111',
            'name': 'Анна Смирнова',
            'email': 'anna@example.com'
        },
        {
            'phone': '+77772222222', 
            'name': 'Михаил Козлов',
            'email': 'mikhail@example.com'
        },
        {
            'phone': '+77773333333',
            'name': 'Елена Воробьева',
            'email': 'elena@example.com'
        },
        {
            'phone': '+77774444444',
            'name': 'Дмитрий Новиков',
            'email': 'dmitry@example.com'
        },
        {
            'phone': '+77775555555',
            'name': 'Ольга Морозова',
            'email': 'olga@example.com'
        }
    ]
    
    customers = []
    for data in customers_data:
        first_name, last_name = data['name'].split(' ', 1)
        customer, created = User.objects.get_or_create(
            phone_number=data['phone'],
            defaults={
                'username': f"customer_{data['phone'][-4:]}",
                'first_name': first_name,
                'last_name': last_name,
                'email': data['email'],
                'user_type': 'customer',
                'is_active': True
            }
        )
        customers.append(customer)
        if created:
            print(f"✅ Создан заказчик: {customer.get_full_name()}")
    
    # Удаляем старые дополнительные тестовые заявки
    old_orders = Order.objects.filter(title__startswith='Дополнительная заявка')
    if old_orders.exists():
        old_orders.delete()
        print("🗑️ Удалены старые дополнительные тестовые заявки")
    
    # Специализированные заявки для разных типов услуг
    specialized_orders = [
        # Фотографы
        {
            'title': 'Свадебная фотосъемка',
            'event_type': 'wedding',
            'description': 'Требуется профессиональный фотограф для свадебной съемки. Нужны красивые кадры в стиле "лайфстайл".',
            'services': ['photographer'],
            'budget_range': (50000, 150000)
        },
        {
            'title': 'Фотосъемка дня рождения',
            'event_type': 'birthday',
            'description': 'Детский день рождения, нужны яркие и веселые фотографии. 2-3 часа съемки.',
            'services': ['photographer'],
            'budget_range': (20000, 60000)
        },
        # Видеографы
        {
            'title': 'Свадебное видео',
            'event_type': 'wedding',
            'description': 'Полный день свадебной видеосъемки с монтажом. Нужен клип и полный фильм.',
            'services': ['videographer'],
            'budget_range': (80000, 200000)
        },
        {
            'title': 'Корпоративное видео',
            'event_type': 'corporate',
            'description': 'Съемка корпоративного мероприятия с последующим монтажом для презентации.',
            'services': ['videographer'],
            'budget_range': (40000, 120000)
        },
        # Ведущие
        {
            'title': 'Ведущий на свадьбу',
            'event_type': 'wedding',
            'description': 'Опытный ведущий для свадебного торжества. Нужна программа с конкурсами и играми.',
            'services': ['host'],
            'budget_range': (30000, 80000)
        },
        {
            'title': 'Ведущий детского праздника',
            'event_type': 'birthday',
            'description': 'Ведущий для детского дня рождения с анимацией и развлекательной программой.',
            'services': ['host'],
            'budget_range': (15000, 40000)
        },
        # Музыканты
        {
            'title': 'Живая музыка на свадьбу',
            'event_type': 'wedding',
            'description': 'Дуэт или трио для свадебного торжества. Классическая и современная музыка.',
            'services': ['musician'],
            'budget_range': (40000, 100000)
        },
        {
            'title': 'DJ для корпоратива',
            'event_type': 'corporate',
            'description': 'DJ для корпоративной вечеринки. Современная музыка, хорошее оборудование.',
            'services': ['musician'],
            'budget_range': (25000, 60000)
        },
        # Рестораны
        {
            'title': 'Банкет в ресторане',
            'event_type': 'wedding',
            'description': 'Организация свадебного банкета на 50-80 человек. Полный сервис.',
            'services': ['restaurant'],
            'budget_range': (200000, 500000)
        },
        {
            'title': 'Корпоративный ужин',
            'event_type': 'corporate',
            'description': 'Организация корпоративного ужина для 30 человек. Бизнес-ланч формат.',
            'services': ['restaurant'],
            'budget_range': (80000, 200000)
        },
        # Шоу-программы
        {
            'title': 'Шоу-программа на юбилей',
            'event_type': 'anniversary',
            'description': 'Развлекательная программа с артистами, фокусниками и танцорами.',
            'services': ['show'],
            'budget_range': (60000, 150000)
        },
        {
            'title': 'Детское шоу',
            'event_type': 'birthday',
            'description': 'Шоу с клоунами, фокусниками и аниматорами для детского праздника.',
            'services': ['show'],
            'budget_range': (30000, 80000)
        },
        # Звезды эстрады
        {
            'title': 'Выступление звезды на свадьбе',
            'event_type': 'wedding',
            'description': 'Приглашение известного артиста для выступления на свадебном торжестве.',
            'services': ['star'],
            'budget_range': (150000, 500000)
        },
        {
            'title': 'Корпоратив со звездой',
            'event_type': 'corporate',
            'description': 'Выступление популярного исполнителя на корпоративном мероприятии.',
            'services': ['star'],
            'budget_range': (100000, 300000)
        }
    ]
    
    venues = [
        'Ресторан "Золотой"', 'Кафе "Уютное"', 'Банкетный зал "Престиж"',
        'Ресторан "Морской"', 'Кафе "Солнечное"', 'Банкетный зал "Элит"',
        'Ресторан "Старый город"', 'Кафе "Весна"', 'Банкетный зал "Люкс"',
        'Ресторан "Панорама"', 'Отель "Астана"', 'Конференц-зал "Бизнес"',
        'Дворец бракосочетаний', 'Парк "Центральный"', 'Клуб "Элитный"'
    ]
    
    orders_created = 0
    
    for i, order_data in enumerate(specialized_orders):
        # Случайная дата в ближайшие 6 месяцев
        days_from_now = random.randint(1, 180)
        event_date = datetime.now().date() + timedelta(days=days_from_now)
        
        # Случайный заказчик
        customer = random.choice(customers)
        
        # Случайный город
        city = random.choice(cities)
        
        # Случайный бюджет в указанном диапазоне
        budget_min = Decimal(random.randint(order_data['budget_range'][0], order_data['budget_range'][1] - 10000))
        budget_max = budget_min + Decimal(random.randint(10000, 20000))
        
        # Создаем заявку
        order = Order.objects.create(
            customer=customer,
            title=f"Дополнительная заявка #{i+1}: {order_data['title']}",
            event_type=order_data['event_type'],
            event_date=event_date,
            venue=random.choice(venues),
            guest_count=random.randint(20, 120),
            description=order_data['description'],
            budget_min=budget_min,
            budget_max=budget_max,
            city=city.name,
            services=order_data['services'],
            status='new',
            order_type='request'
        )
        
        orders_created += 1
        print(f"✅ Создана специализированная заявка: {order.title} ({city.name})")
    
    # Добавляем еще несколько случайных заявок
    for i in range(10):
        days_from_now = random.randint(1, 120)
        event_date = datetime.now().date() + timedelta(days=days_from_now)
        
        customer = random.choice(customers)
        city = random.choice(cities)
        service_type = random.choice(service_types)
        
        budget_min = Decimal(random.randint(25000, 120000))
        budget_max = budget_min + Decimal(random.randint(15000, 40000))
        
        order = Order.objects.create(
            customer=customer,
            title=f"Дополнительная заявка #{orders_created + i + 1}: Случайное мероприятие",
            event_type=random.choice(['wedding', 'birthday', 'corporate', 'anniversary', 'graduation', 'party']),
            event_date=event_date,
            venue=random.choice(venues),
            guest_count=random.randint(15, 100),
            description=f"Случайная заявка для тестирования. Требуется профессиональный исполнитель.",
            budget_min=budget_min,
            budget_max=budget_max,
            city=city.name,
            services=[service_type.code],
            status='new',
            order_type='request'
        )
        
        orders_created += 1
        print(f"✅ Создана случайная заявка: {order.title} ({city.name}, {service_type.name})")
    
    print(f"\n🎉 Успешно создано {orders_created} дополнительных тестовых заявок!")
    print(f"📊 Общая статистика:")
    total_orders = Order.objects.filter(title__startswith='Тестовая заявка').count() + Order.objects.filter(title__startswith='Дополнительная заявка').count()
    print(f"   - Всего тестовых заявок: {total_orders}")
    print(f"   - Заказчиков: {len(customers)}")
    print(f"   - Города: {', '.join(set([order.city for order in Order.objects.filter(title__startswith='Дополнительная заявка')]))}")
    print(f"   - Типы услуг: {', '.join(set([service_type.name for service_type in service_types]))}")

if __name__ == '__main__':
    print("🚀 Добавление дополнительных тестовых заявок...")
    add_more_test_orders()
    print("✅ Готово!") 