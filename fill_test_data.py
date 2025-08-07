#!/usr/bin/env python
import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, City, ServiceType, Order, Portfolio, Tariff, BusyDate, Review, OrderResponse
from django.contrib.auth.hashers import make_password

def create_test_data():
    print("🎯 Создание тестовых данных для личного кабинета...")
    
    # Получаем существующие города и типы услуг
    cities = list(City.objects.filter(is_active=True))
    service_types = list(ServiceType.objects.filter(is_active=True))
    
    if not cities or not service_types:
        print("❌ Ошибка: Нет городов или типов услуг в базе данных!")
        return
    
    # Создаем тестового исполнителя
    print("👤 Создание тестового исполнителя...")
    performer = User.objects.create_user(
        username='test_performer',
        email='performer@test.com',
        password='testpass123',
        phone_number='+77771234567',
        first_name='Александр',
        last_name='Петров',
        user_type='performer',
        city=random.choice(cities),
        service_type=random.choice(service_types),
        company_name='Студия "Праздник"',
        bio='Профессиональный фотограф с 5-летним опытом. Специализируюсь на свадебной и семейной фотографии. Создаю незабываемые моменты для ваших особенных дней.',
        rating=4.8
    )
    
    # Создаем тестового заказчика
    print("👤 Создание тестового заказчика...")
    customer = User.objects.create_user(
        username='test_customer',
        email='customer@test.com',
        password='testpass123',
        phone_number='+77776543210',
        first_name='Мария',
        last_name='Иванова',
        user_type='customer',
        city=random.choice(cities),
        bio='Люблю организовывать красивые мероприятия для друзей и семьи.'
    )
    
    # Создаем портфолио (15 фотографий)
    print("📸 Создание портфолио...")
    portfolio_photos = [
        'portfolio/customer_portfolio_1.jpg',
        'portfolio/customer_portfolio_2.jpg',
        'portfolio/ChatGPT_Image_16_апр._2025_г._14_11_02.png',
        'portfolio/customer_portfolio_3.jpg',
        'portfolio/customer_portfolio_4.jpg',
        'portfolio/customer_portfolio_5.jpg',
        'portfolio/customer_portfolio_6.jpg',
        'portfolio/customer_portfolio_7.jpg',
        'portfolio/customer_portfolio_8.jpg',
        'portfolio/customer_portfolio_9.jpg',
        'portfolio/customer_portfolio_10.jpg',
        'portfolio/customer_portfolio_11.jpg',
        'portfolio/customer_portfolio_12.jpg',
        'portfolio/customer_portfolio_13.jpg',
        'portfolio/customer_portfolio_14.jpg',
    ]
    
    for i, photo_path in enumerate(portfolio_photos):
        try:
            Portfolio.objects.create(
                user=performer,
                image=photo_path
            )
        except:
            # Если файл не существует, создаем запись без изображения
            Portfolio.objects.create(
                user=performer
            )
    
    # Создаем тарифы (5 тарифов)
    print("💰 Создание тарифов...")
    tariff_names = [
        'Базовый пакет',
        'Стандартный пакет', 
        'Премиум пакет',
        'VIP пакет',
        'Свадебный пакет'
    ]
    
    for i, name in enumerate(tariff_names):
        Tariff.objects.create(
            user=performer,
            name=name,
            price=Decimal(50000 + i * 25000),
            description=f'Описание для тарифа "{name}". Включает профессиональную съемку, обработку фотографий и базовое оформление.'
        )
    
    # Создаем занятые даты (10 дат)
    print("📅 Создание занятых дат...")
    busy_dates = []
    for i in range(10):
        date = datetime.now().date() + timedelta(days=random.randint(1, 60))
        if date not in busy_dates:
            BusyDate.objects.create(
                user=performer,
                date=date
            )
            busy_dates.append(date)
    
    # Создаем заказы (8 заказов)
    print("📋 Создание заказов...")
    order_titles = [
        'Свадьба Анны и Михаила',
        'День рождения ребенка',
        'Корпоративное мероприятие',
        'Юбилей бабушки',
        'Выпускной вечер',
        'Романтическое предложение',
        'Семейная фотосессия',
        'Празднование Нового года'
    ]
    
    event_types = ['wedding', 'birthday', 'corporate', 'anniversary', 'graduation', 'proposal', 'family', 'holiday']
    
    for i, title in enumerate(order_titles):
        order = Order.objects.create(
            customer=customer,
            title=title,
            event_type=event_types[i % len(event_types)],
            event_date=datetime.now().date() + timedelta(days=random.randint(10, 90)),
            venue=f'Ресторан "{random.choice(["Золотой", "Серебряный", "Бриллиант", "Рубин", "Сапфир"])}"',
            guest_count=random.randint(20, 150),
            description=f'Подробное описание мероприятия: {title}. Требуется профессиональная съемка и оформление.',
            budget_min=Decimal(50000 + random.randint(0, 100000)),
            budget_max=Decimal(150000 + random.randint(0, 200000)),
            city=random.choice(cities).name,
            services=random.sample([st.code for st in service_types], random.randint(1, 3)),
            status=random.choice(['new', 'in_progress', 'completed']),
            order_type='request'
        )
        
        # Создаем отклики на заказы (2-4 отклика на заказ)
        for j in range(random.randint(2, 4)):
            other_performer = User.objects.create_user(
                username=f'performer_{i}_{j}',
                email=f'performer_{i}_{j}@test.com',
                password='testpass123',
                phone_number=f'+7777{random.randint(1000000, 9999999)}',
                first_name=random.choice(['Андрей', 'Дмитрий', 'Сергей', 'Владимир', 'Николай']),
                last_name=random.choice(['Смирнов', 'Козлов', 'Новиков', 'Морозов', 'Петров']),
                user_type='performer',
                city=random.choice(cities),
                service_type=random.choice(service_types),
                rating=round(random.uniform(3.5, 5.0), 1)
            )
            
            OrderResponse.objects.create(
                performer=other_performer,
                order=order,
                price=Decimal(random.randint(30000, 200000)),
                message=f'Здравствуйте! Готов выполнить ваш заказ "{title}". У меня есть опыт в подобных мероприятиях.'
            )
    
    # Создаем активные заказы исполнителя (3 заказа)
    print("✅ Создание активных заказов исполнителя...")
    active_order_titles = [
        'Свадьба Елены и Дмитрия',
        'Корпоратив IT-компании',
        'День рождения мамы'
    ]
    
    for i, title in enumerate(active_order_titles):
        Order.objects.create(
            customer=customer,
            performer=performer,
            title=title,
            event_type=random.choice(event_types),
            event_date=datetime.now().date() + timedelta(days=random.randint(5, 30)),
            venue=f'Банкетный зал "{random.choice(["Элегант", "Люкс", "Престиж", "Гранд", "Эксклюзив"])}"',
            guest_count=random.randint(30, 100),
            description=f'Активный заказ: {title}. Исполнитель уже назначен.',
            budget_min=Decimal(80000 + random.randint(0, 50000)),
            budget_max=Decimal(180000 + random.randint(0, 100000)),
            city=random.choice(cities).name,
            services=[performer.service_type.code] if performer.service_type else [],
            status=random.choice(['new', 'in_progress']),
            order_type='booking'
        )
    
    # Создаем отклики исполнителя на заказы (5 откликов)
    print("💬 Создание откликов исполнителя...")
    for i in range(5):
        order = Order.objects.filter(status='new', order_type='request').first()
        if order:
            OrderResponse.objects.create(
                performer=performer,
                order=order,
                price=Decimal(random.randint(50000, 150000)),
                message=f'Здравствуйте! Я готов выполнить ваш заказ "{order.title}". У меня большой опыт в подобных мероприятиях.'
            )
    
    # Создаем отзывы (8 отзывов)
    print("⭐ Создание отзывов...")
    review_texts = [
        'Отличный исполнитель! Все было на высшем уровне.',
        'Профессионал своего дела. Рекомендую!',
        'Очень довольны результатом. Спасибо!',
        'Качественная работа, все в срок.',
        'Прекрасный фотограф, красивые снимки.',
        'Вежливый и пунктуальный исполнитель.',
        'Все прошло идеально, спасибо!',
        'Отличное качество услуг.'
    ]
    
    for i in range(8):
        Review.objects.create(
            from_user=customer,
            to_user=performer,
            order=Order.objects.filter(customer=customer).first(),
            rating=random.randint(4, 5),
            comment=review_texts[i % len(review_texts)]
        )
    
    # Создаем дополнительные исполнители для каталога (10 исполнителей)
    print("👥 Создание дополнительных исполнителей...")
    for i in range(10):
        performer_name = random.choice(['Анна', 'Елена', 'Ольга', 'Татьяна', 'Ирина', 'Наталья', 'Марина', 'Светлана', 'Юлия', 'Алена'])
        performer_surname = random.choice(['Кузнецова', 'Соколова', 'Лебедева', 'Козлова', 'Новикова', 'Морозова', 'Петрова', 'Волкова', 'Соловьева', 'Васильева'])
        
        new_performer = User.objects.create_user(
            username=f'performer_catalog_{i}',
            email=f'performer_catalog_{i}@test.com',
            password='testpass123',
            phone_number=f'+7777{random.randint(1000000, 9999999)}',
            first_name=performer_name,
            last_name=performer_surname,
            user_type='performer',
            city=random.choice(cities),
            service_type=random.choice(service_types),
            company_name=f'Студия "{random.choice(["Радость", "Улыбка", "Счастье", "Праздник", "Мечта"])}"',
            bio=f'Профессиональный {random.choice(["фотограф", "видеограф", "музыкант", "ведущий"])} с опытом работы.',
            rating=round(random.uniform(3.8, 5.0), 1)
        )
        
        # Создаем тарифы для каждого исполнителя
        for j in range(random.randint(1, 3)):
            Tariff.objects.create(
                user=new_performer,
                name=f'Пакет {j+1}',
                price=Decimal(30000 + j * 20000),
                description=f'Описание пакета {j+1}'
            )
    
    print("\n🎉 Тестовые данные успешно созданы!")
    print(f"✅ Исполнитель: {performer.get_full_name()} (логин: test_performer, пароль: testpass123)")
    print(f"✅ Заказчик: {customer.get_full_name()} (логин: test_customer, пароль: testpass123)")
    print(f"📸 Портфолио: {Portfolio.objects.filter(user=performer).count()} фотографий")
    print(f"💰 Тарифы: {Tariff.objects.filter(user=performer).count()} тарифов")
    print(f"📅 Занятые даты: {BusyDate.objects.filter(user=performer).count()} дат")
    print(f"📋 Заказы: {Order.objects.count()} заказов")
    print(f"💬 Отклики: {OrderResponse.objects.count()} откликов")
    print(f"⭐ Отзывы: {Review.objects.count()} отзывов")
    print(f"👥 Исполнителей в каталоге: {User.objects.filter(user_type='performer').count()}")
    
    print("\n🚀 Теперь можете войти в личный кабинет и посмотреть на полной нагрузке!")

if __name__ == '__main__':
    create_test_data() 