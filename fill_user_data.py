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

def fill_user_data():
    print("🎯 Заполнение данными для пользователя +77085446945...")
    
    # Находим пользователя
    user = User.objects.filter(phone_number='+77085446945').first()
    if not user:
        print("❌ Пользователь с номером +77085446945 не найден!")
        return
    
    print(f"✅ Найден пользователь: {user.get_full_name()} ({user.user_type})")
    
    # Получаем существующие города и типы услуг
    cities = list(City.objects.filter(is_active=True))
    service_types = list(ServiceType.objects.filter(is_active=True))
    
    if not cities or not service_types:
        print("❌ Ошибка: Нет городов или типов услуг в базе данных!")
        return
    
    # Если пользователь исполнитель, создаем для него данные
    if user.user_type == 'performer':
        print("👤 Заполнение данных для исполнителя...")
        
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
        
        # Удаляем существующие записи портфолио
        Portfolio.objects.filter(user=user).delete()
        
        for i, photo_path in enumerate(portfolio_photos):
            try:
                Portfolio.objects.create(
                    user=user,
                    image=photo_path
                )
            except:
                # Если файл не существует, создаем запись без изображения
                Portfolio.objects.create(
                    user=user
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
        
        # Удаляем существующие тарифы
        Tariff.objects.filter(user=user).delete()
        
        for i, name in enumerate(tariff_names):
            Tariff.objects.create(
                user=user,
                name=name,
                price=Decimal(50000 + i * 25000),
                description=f'Описание для тарифа "{name}". Включает профессиональную съемку, обработку фотографий и базовое оформление.'
            )
        
        # Создаем занятые даты (10 дат)
        print("📅 Создание занятых дат...")
        BusyDate.objects.filter(user=user).delete()
        
        busy_dates = []
        for i in range(10):
            date = datetime.now().date() + timedelta(days=random.randint(1, 60))
            if date not in busy_dates:
                BusyDate.objects.create(
                    user=user,
                    date=date
                )
                busy_dates.append(date)
        
        # Создаем отзывы (8 отзывов)
        print("⭐ Создание отзывов...")
        Review.objects.filter(to_user=user).delete()
        
        # Создаем тестового заказчика для отзывов
        customer = User.objects.filter(user_type='customer').first()
        if not customer:
            customer = User.objects.create_user(
                username='test_customer_for_reviews',
                email='customer_reviews@test.com',
                password='testpass123',
                phone_number='+77776543210',
                first_name='Мария',
                last_name='Иванова',
                user_type='customer',
                city=random.choice(cities)
            )
        
        # Создаем заказы для отзывов
        review_orders = []
        for i in range(8):
            order = Order.objects.create(
                customer=customer,
                performer=user,
                title=f'Заказ для отзыва #{i+1}',
                event_type=random.choice(['wedding', 'birthday', 'corporate', 'anniversary']),
                event_date=datetime.now().date() - timedelta(days=random.randint(1, 30)),
                venue=f'Ресторан "{random.choice(["Золотой", "Серебряный", "Бриллиант"])}"',
                guest_count=random.randint(20, 100),
                description=f'Заказ для отзыва #{i+1}. Мероприятие прошло успешно.',
                budget_min=Decimal(50000 + random.randint(0, 50000)),
                budget_max=Decimal(150000 + random.randint(0, 50000)),
                city=random.choice(cities).name,
                services=[user.service_type.code] if user.service_type else [],
                status='completed',
                order_type='booking'
            )
            review_orders.append(order)
        
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
                to_user=user,
                order=review_orders[i],
                rating=random.randint(4, 5),
                comment=review_texts[i % len(review_texts)]
            )
        
        # Создаем активные заказы (3 заказа)
        print("✅ Создание активных заказов...")
        active_order_titles = [
            'Свадьба Елены и Дмитрия',
            'Корпоратив IT-компании',
            'День рождения мамы'
        ]
        
        event_types = ['wedding', 'birthday', 'corporate', 'anniversary', 'graduation', 'proposal', 'family', 'holiday']
        
        for i, title in enumerate(active_order_titles):
            Order.objects.create(
                customer=customer,
                performer=user,
                title=title,
                event_type=random.choice(event_types),
                event_date=datetime.now().date() + timedelta(days=random.randint(5, 30)),
                venue=f'Банкетный зал "{random.choice(["Элегант", "Люкс", "Престиж", "Гранд", "Эксклюзив"])}"',
                guest_count=random.randint(30, 100),
                description=f'Активный заказ: {title}. Исполнитель уже назначен.',
                budget_min=Decimal(80000 + random.randint(0, 50000)),
                budget_max=Decimal(180000 + random.randint(0, 100000)),
                city=random.choice(cities).name,
                services=[user.service_type.code] if user.service_type else [],
                status=random.choice(['new', 'in_progress']),
                order_type='booking'
            )
        
        # Создаем отклики на заказы (5 откликов)
        print("💬 Создание откликов на заказы...")
        OrderResponse.objects.filter(performer=user).delete()
        
        # Создаем несколько заказов для откликов
        for i in range(5):
            order = Order.objects.create(
                customer=customer,
                title=f'Заказ для отклика #{i+1}',
                event_type=random.choice(event_types),
                event_date=datetime.now().date() + timedelta(days=random.randint(10, 90)),
                venue=f'Ресторан "{random.choice(["Золотой", "Серебряный", "Бриллиант"])}"',
                guest_count=random.randint(20, 150),
                description=f'Заказ для отклика #{i+1}. Требуется профессиональная съемка.',
                budget_min=Decimal(50000 + random.randint(0, 100000)),
                budget_max=Decimal(150000 + random.randint(0, 200000)),
                city=random.choice(cities).name,
                services=random.sample([st.code for st in service_types], random.randint(1, 3)),
                status='new',
                order_type='request'
            )
            
            OrderResponse.objects.create(
                performer=user,
                order=order,
                price=Decimal(random.randint(50000, 150000)),
                message=f'Здравствуйте! Я готов выполнить ваш заказ "{order.title}". У меня большой опыт в подобных мероприятиях.'
            )
    
    # Если пользователь заказчик, создаем для него заказы
    elif user.user_type == 'customer':
        print("👤 Заполнение данных для заказчика...")
        
        # Создаем заказы для заказчика
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
                customer=user,
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
                other_performer = User.objects.filter(user_type='performer').first()
                if not other_performer:
                    other_performer = User.objects.create_user(
                        username=f'performer_for_responses_{i}_{j}',
                        email=f'performer_responses_{i}_{j}@test.com',
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
    
    print("\n🎉 Данные успешно заполнены для пользователя +77085446945!")
    print(f"👤 Пользователь: {user.get_full_name()} ({user.user_type})")
    
    if user.user_type == 'performer':
        print(f"📸 Портфолио: {Portfolio.objects.filter(user=user).count()} фотографий")
        print(f"💰 Тарифы: {Tariff.objects.filter(user=user).count()} тарифов")
        print(f"📅 Занятые даты: {BusyDate.objects.filter(user=user).count()} дат")
        print(f"⭐ Отзывы: {Review.objects.filter(to_user=user).count()} отзывов")
        print(f"✅ Активные заказы: {Order.objects.filter(performer=user).count()} заказов")
        print(f"💬 Отклики: {OrderResponse.objects.filter(performer=user).count()} откликов")
    elif user.user_type == 'customer':
        print(f"📋 Заказы: {Order.objects.filter(customer=user).count()} заказов")
        print(f"💬 Отклики на заказы: {OrderResponse.objects.filter(order__customer=user).count()} откликов")
    
    print("\n🚀 Теперь можете войти в личный кабинет и посмотреть на полной нагрузке!")

if __name__ == '__main__':
    fill_user_data() 