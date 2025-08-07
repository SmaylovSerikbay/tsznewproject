#!/usr/bin/env python
import os
import sys
import django
import random
import requests
from datetime import date, timedelta
from decimal import Decimal
from io import BytesIO
from django.core.files import File

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Portfolio, Tariff, BusyDate, ServiceType, City
from django.contrib.auth.hashers import make_password

def download_image(url, filename):
    """Скачивает изображение по URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return File(BytesIO(response.content), name=filename)
    except Exception as e:
        print(f"Ошибка при скачивании изображения {url}: {e}")
        return None

def generate_kazakh_phone():
    """Генерирует случайный казахстанский номер телефона"""
    prefixes = ['+7700', '+7701', '+7702', '+7705', '+7707', '+7708', '+7710', '+7711', '+7712', '+7713', '+7714', '+7715', '+7716', '+7717', '+7718', '+7719', '+7720', '+7721', '+7722', '+7723', '+7724', '+7725', '+7726', '+7727', '+7728', '+7729', '+7730', '+7731', '+7732', '+7733', '+7734', '+7735', '+7736', '+7737', '+7738', '+7739', '+7740', '+7741', '+7742', '+7743', '+7744', '+7745', '+7746', '+7747', '+7748', '+7749', '+7750', '+7751', '+7752', '+7753', '+7754', '+7755', '+7756', '+7757', '+7758', '+7759', '+7760', '+7761', '+7762', '+7763', '+7764', '+7765', '+7766', '+7767', '+7768', '+7769', '+7770', '+7771', '+7772', '+7773', '+7774', '+7775', '+7776', '+7777', '+7778', '+7779', '+7780', '+7781', '+7782', '+7783', '+7784', '+7785', '+7786', '+7787', '+7788', '+7789', '+7790', '+7791', '+7792', '+7793', '+7794', '+7795', '+7796', '+7797', '+7798', '+7799']
    prefix = random.choice(prefixes)
    number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"{prefix}{number}"

def create_kazakh_performers():
    """Создает казахстанских исполнителей с реальными данными"""
    
    # Данные исполнителей
    performers_data = [
        {
            'name': 'Дос',
            'full_name': 'Досымжан Жолдасбеков',
            'service_type': 'star',
            'city': 'Алматы',
            'company': 'Дос Entertainment',
            'bio': 'Известный казахстанский певец и композитор. Участник группы "Дос-Мукасан". Автор множества популярных песен. Выступает на свадьбах, корпоративах и концертах.',
            'rating': 4.9,
            'profile_photo': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Баглан',
            'full_name': 'Баглан Абдраймов',
            'service_type': 'star',
            'city': 'Астана',
            'company': 'Баглан Music',
            'bio': 'Популярный казахстанский певец и музыкант. Известен своими лирическими песнями и красивым голосом. Выступает на различных мероприятиях.',
            'rating': 4.8,
            'profile_photo': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Айдар',
            'full_name': 'Айдар Тургамбек',
            'service_type': 'star',
            'city': 'Алматы',
            'company': 'Айдар Show',
            'bio': 'Талантливый певец и артист. Известен своими энергичными выступлениями и харизматичным стилем. Создает незабываемую атмосферу на любом мероприятии.',
            'rating': 4.7,
            'profile_photo': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Аскар',
            'full_name': 'Аскар Жайлаубаев',
            'service_type': 'star',
            'city': 'Караганда',
            'company': 'Аскар Music Studio',
            'bio': 'Профессиональный певец с уникальным голосом. Специализируется на казахских народных песнях и современной музыке. Выступает на национальных праздниках и торжествах.',
            'rating': 4.9,
            'profile_photo': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Бауыржан',
            'full_name': 'Бауыржан Исаев',
            'service_type': 'star',
            'city': 'Алматы',
            'company': 'Бауыржан Entertainment',
            'bio': 'Известный певец и композитор. Автор множества хитов. Выступает на свадьбах, корпоративах и концертах. Создает особую атмосферу на каждом мероприятии.',
            'rating': 4.8,
            'profile_photo': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Бауыржан Н.',
            'full_name': 'Бауыржан Нурымбетов',
            'service_type': 'star',
            'city': 'Астана',
            'company': 'Бауыржан N Music',
            'bio': 'Талантливый певец с красивым голосом. Специализируется на романтических песнях и лирических композициях. Идеально подходит для свадеб и романтических вечеров.',
            'rating': 4.6,
            'profile_photo': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Маржан',
            'full_name': 'Маржан Арапбаева',
            'service_type': 'star',
            'city': 'Алматы',
            'company': 'Маржан Voice',
            'bio': 'Очаровательная певица с прекрасным голосом. Известна своими лирическими песнями и красивыми мелодиями. Выступает на различных мероприятиях и создает романтическую атмосферу.',
            'rating': 4.9,
            'profile_photo': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Кыдырали',
            'full_name': 'Кыдырали Болманов',
            'service_type': 'star',
            'city': 'Шымкент',
            'company': 'Кыдырали Show',
            'bio': 'Энергичный певец и артист. Известен своими зажигательными выступлениями и позитивной энергетикой. Идеально подходит для веселых мероприятий и праздников.',
            'rating': 4.7,
            'profile_photo': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Каракат',
            'full_name': 'Каракат Абильдина',
            'service_type': 'star',
            'city': 'Алматы',
            'company': 'Каракат Music',
            'bio': 'Талантливая певица с уникальным голосом. Специализируется на казахских народных песнях и современной музыке. Создает особую атмосферу на национальных праздниках.',
            'rating': 4.8,
            'profile_photo': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Курмаш',
            'full_name': 'Курмаш Маханов',
            'service_type': 'star',
            'city': 'Астана',
            'company': 'Курмаш Entertainment',
            'bio': 'Профессиональный певец и музыкант. Известен своими красивыми песнями и профессиональным подходом к каждому выступлению. Выступает на свадьбах и корпоративах.',
            'rating': 4.6,
            'profile_photo': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Ерлан',
            'full_name': 'Ерлан Малаев',
            'service_type': 'star',
            'city': 'Алматы',
            'company': 'Ерлан Voice Studio',
            'bio': 'Талантливый певец с глубоким голосом. Специализируется на романтических и лирических песнях. Создает незабываемую атмосферу на свадьбах и романтических вечерах.',
            'rating': 4.7,
            'profile_photo': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Зарина',
            'full_name': 'Зарина Омарова',
            'service_type': 'star',
            'city': 'Астана',
            'company': 'Зарина Music',
            'bio': 'Очаровательная певица с прекрасным голосом. Известна своими красивыми песнями и профессиональными выступлениями. Идеально подходит для элегантных мероприятий.',
            'rating': 4.9,
            'profile_photo': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Алтынай',
            'full_name': 'Алтынай Жорабаева',
            'service_type': 'star',
            'city': 'Алматы',
            'company': 'Алтынай Voice',
            'bio': 'Талантливая певица с уникальным стилем. Специализируется на современной музыке и казахских песнях. Создает особую атмосферу на каждом мероприятии.',
            'rating': 4.8,
            'profile_photo': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        },
        {
            'name': 'Лукпан',
            'full_name': 'Лукпан Жолдасов',
            'service_type': 'star',
            'city': 'Караганда',
            'company': 'Лукпан Show',
            'bio': 'Энергичный певец и артист. Известен своими зажигательными выступлениями и позитивной энергетикой. Идеально подходит для веселых мероприятий и праздников.',
            'rating': 4.7,
            'profile_photo': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face',
            'portfolio_photos': [
                'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop'
            ]
        }
    ]
    
    print("🎤 Создание казахстанских исполнителей...")
    
    # Получаем тип услуги "Звезды Эстрады"
    try:
        service_type = ServiceType.objects.get(code='star')
    except ServiceType.DoesNotExist:
        print("❌ Тип услуги 'star' не найден!")
        return
    
    created_performers = []
    
    for performer_data in performers_data:
        # Генерируем уникальный номер телефона
        phone_number = generate_kazakh_phone()
        while User.objects.filter(phone_number=phone_number).exists():
            phone_number = generate_kazakh_phone()
        
        # Получаем город
        try:
            city = City.objects.get(name=performer_data['city'])
        except City.DoesNotExist:
            print(f"❌ Город {performer_data['city']} не найден!")
            continue
        
        # Разделяем полное имя на имя и фамилию
        name_parts = performer_data['full_name'].split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Создаем пользователя
        username = f"performer_{phone_number.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')}"
        
        performer = User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password='performer123456',
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            city=city,
            user_type='performer',
            service_type=service_type,
            company_name=performer_data['company'],
            bio=performer_data['bio'],
            is_phone_verified=True,
            rating=performer_data['rating']
        )
        
        print(f"✅ Создан исполнитель: {performer.get_full_name()} ({phone_number})")
        
        # Скачиваем и устанавливаем фото профиля
        profile_photo = download_image(performer_data['profile_photo'], f'{username}_profile.jpg')
        if profile_photo:
            performer.profile_photo.save(f'{username}_profile.jpg', profile_photo, save=True)
            print(f"   📸 Установлено фото профиля")
        
        # Создаем портфолио
        for i, photo_url in enumerate(performer_data['portfolio_photos']):
            portfolio_photo = download_image(photo_url, f'{username}_portfolio_{i+1}.jpg')
            if portfolio_photo:
                Portfolio.objects.create(
                    user=performer,
                    image=portfolio_photo
                )
                print(f"   🖼️ Добавлено фото в портфолио {i+1}")
        
        # Создаем тарифы
        base_price = random.randint(80000, 150000)
        tariff1 = Tariff.objects.create(
            user=performer,
            name='Базовый пакет',
            price=Decimal(str(base_price)),
            description='1 час выступления, 5-7 песен, базовое оборудование'
        )
        
        tariff2 = Tariff.objects.create(
            user=performer,
            name='Стандартный пакет',
            price=Decimal(str(base_price + 20000)),
            description='2 часа выступления, 10-12 песен, полное оборудование'
        )
        
        tariff3 = Tariff.objects.create(
            user=performer,
            name='Премиум пакет',
            price=Decimal(str(base_price + 50000)),
            description='3 часа выступления, 15-20 песен, полное оборудование, интермедия'
        )
        
        print(f"   💰 Созданы тарифы: {tariff1.price}₸, {tariff2.price}₸, {tariff3.price}₸")
        
        # Добавляем несколько занятых дат
        busy_dates = []
        for i in range(random.randint(3, 8)):
            busy_date = date.today() + timedelta(days=random.randint(1, 60))
            if busy_date not in busy_dates:
                BusyDate.objects.create(
                    user=performer,
                    date=busy_date
                )
                busy_dates.append(busy_date)
        
        print(f"   📅 Добавлено {len(busy_dates)} занятых дат")
        
        created_performers.append(performer)
        print(f"   ⭐ Рейтинг: {performer.rating}")
        print()
    
    print(f"🎉 Успешно создано {len(created_performers)} казахстанских исполнителей!")
    print("\n📋 Список созданных исполнителей:")
    for performer in created_performers:
        print(f"   • {performer.get_full_name()} - {performer.phone_number} - {performer.city.name}")

if __name__ == "__main__":
    create_kazakh_performers() 