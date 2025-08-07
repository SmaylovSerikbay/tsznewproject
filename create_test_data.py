#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Order, Review, OrderResponse

def create_test_data():
    print("Создание дополнительных тестовых данных...")
    
    # Получаем созданных пользователей
    customer = User.objects.get(username='customer_test')
    photographer = User.objects.get(username='photographer_test')
    host = User.objects.get(username='host_test')
    musician = User.objects.get(username='musician_test')
    
    # Создаем тестовые заказы
    order1 = Order.objects.create(
        customer=customer,
        title='Свадьба Алексея и Елены',
        event_type='wedding',
        event_date=date.today() + timedelta(days=30),
        city='Алматы',
        venue='Ресторан "Золотой"',
        guest_count=100,
        description='Торжественная свадьба в классическом стиле. Нужны фотограф и ведущий для создания незабываемой атмосферы.',
        budget_min=Decimal('100000'),
        budget_max=Decimal('200000'),
        services=['photo', 'host'],
        status='new',
        order_type='request'
    )
    print(f"✅ Создан заказ: {order1.title}")
    
    order2 = Order.objects.create(
        customer=customer,
        title='День рождения дочери',
        event_type='birthday',
        event_date=date.today() + timedelta(days=45),
        city='Алматы',
        venue='Кафе "Сказка"',
        guest_count=25,
        description='День рождения дочери 10 лет. Нужен ведущий для детских игр и конкурсов.',
        budget_min=Decimal('30000'),
        budget_max=Decimal('50000'),
        services=['host'],
        status='new',
        order_type='request'
    )
    print(f"✅ Создан заказ: {order2.title}")
    
    order3 = Order.objects.create(
        customer=customer,
        title='Корпоративный ужин',
        event_type='corporate',
        event_date=date.today() + timedelta(days=60),
        city='Алматы',
        venue='Офис компании',
        guest_count=15,
        description='Корпоративный ужин для команды. Нужна живая музыка для создания приятной атмосферы.',
        budget_min=Decimal('25000'),
        budget_max=Decimal('40000'),
        services=['music'],
        status='new',
        order_type='request'
    )
    print(f"✅ Создан заказ: {order3.title}")
    
    # Создаем отклики исполнителей на заказы
    response1 = OrderResponse.objects.create(
        order=order1,
        performer=photographer,
        message='Здравствуйте! Готова провести съемку вашей свадьбы. Предлагаю премиум пакет с полным днем съемки.',
        price=Decimal('120000')
    )
    print(f"✅ Создан отклик фотографа на заказ 1")
    
    response2 = OrderResponse.objects.create(
        order=order1,
        performer=host,
        message='Добрый день! С удовольствием проведу вашу свадьбу. Создам незабываемую атмосферу с конкурсами и играми.',
        price=Decimal('60000')
    )
    print(f"✅ Создан отклик ведущего на заказ 1")
    
    response3 = OrderResponse.objects.create(
        order=order2,
        performer=host,
        message='Привет! Специализируюсь на детских праздниках. Проведу веселые конкурсы и игры для детей.',
        price=Decimal('40000')
    )
    print(f"✅ Создан отклик ведущего на заказ 2")
    
    response4 = OrderResponse.objects.create(
        order=order3,
        performer=musician,
        message='Здравствуйте! Наша группа готова создать приятную атмосферу для вашего корпоратива.',
        price=Decimal('35000')
    )
    print(f"✅ Создан отклик музыканта на заказ 3")
    
    # Создаем завершенный заказ с отзывами
    completed_order = Order.objects.create(
        customer=customer,
        performer=photographer,
        title='Свадьба друзей',
        event_type='wedding',
        event_date=date.today() - timedelta(days=30),
        city='Алматы',
        venue='Банкетный зал "Рояль"',
        guest_count=80,
        description='Свадьба друзей, которая уже прошла. Фотограф отлично справился с задачей.',
        budget_min=Decimal('80000'),
        budget_max=Decimal('100000'),
        services=['photo'],
        status='completed',
        order_type='booking'
    )
    print(f"✅ Создан завершенный заказ: {completed_order.title}")
    
    # Создаем отзывы
    review1 = Review.objects.create(
        order=completed_order,
        from_user=customer,
        to_user=photographer,
        rating=5,
        comment='Отличная работа! Фотографии получились просто великолепные. Мария очень профессионально подошла к делу, все гости остались довольны. Рекомендую всем!'
    )
    print(f"✅ Создан отзыв от заказчика к фотографу")
    
    review2 = Review.objects.create(
        order=completed_order,
        from_user=photographer,
        to_user=customer,
        rating=5,
        comment='Приятно было работать с Алексеем. Все было организовано четко, гости были дружелюбными. Спасибо за доверие!'
    )
    print(f"✅ Создан отзыв от фотографа к заказчику")
    
    # Создаем еще один завершенный заказ с ведущим
    completed_order2 = Order.objects.create(
        customer=customer,
        performer=host,
        title='Юбилей бабушки',
        event_type='birthday',
        event_date=date.today() - timedelta(days=15),
        city='Алматы',
        venue='Дом',
        guest_count=20,
        description='Юбилей бабушки прошел отлично благодаря ведущему Дмитрию.',
        budget_min=Decimal('40000'),
        budget_max=Decimal('50000'),
        services=['host'],
        status='completed',
        order_type='booking'
    )
    print(f"✅ Создан завершенный заказ: {completed_order2.title}")
    
    review3 = Review.objects.create(
        order=completed_order2,
        from_user=customer,
        to_user=host,
        rating=5,
        comment='Дмитрий просто супер! Бабушка была в восторге, все гости веселились от души. Очень душевно и профессионально провел праздник.'
    )
    print(f"✅ Создан отзыв от заказчика к ведущему")
    
    review4 = Review.objects.create(
        order=completed_order2,
        from_user=host,
        to_user=customer,
        rating=5,
        comment='Спасибо за теплый прием! Было очень приятно работать с такой дружной семьей. Бабушка - просто чудо!'
    )
    print(f"✅ Создан отзыв от ведущего к заказчику")
    
    print("\n" + "="*50)
    print("🎉 ДОПОЛНИТЕЛЬНЫЕ ТЕСТОВЫЕ ДАННЫЕ СОЗДАНЫ!")
    print("="*50)
    print("\n📋 СОЗДАННЫЕ ДАННЫЕ:")
    print(f"   Новые заказы: 3")
    print(f"   Отклики исполнителей: 4")
    print(f"   Завершенные заказы: 2")
    print(f"   Отзывы: 4")
    
    print("\n📝 ДЕТАЛИ ЗАКАЗОВ:")
    print(f"   1. Свадьба Алексея и Елены (30 дней) - нужны фотограф и ведущий")
    print(f"   2. День рождения дочери (45 дней) - нужен ведущий")
    print(f"   3. Корпоративный ужин (60 дней) - нужна живая музыка")
    
    print("\n✅ ЗАВЕРШЕННЫЕ ЗАКАЗЫ:")
    print(f"   1. Свадьба друзей (прошла 30 дней назад) - фотограф")
    print(f"   2. Юбилей бабушки (прошло 15 дней назад) - ведущий")
    
    print("\n🌐 ССЫЛКА НА САЙТ:")
    print("   http://localhost:8000")
    
    print("\n" + "="*50)

if __name__ == '__main__':
    create_test_data() 