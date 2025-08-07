#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import City

def add_cities():
    """Добавляет города в базу данных"""
    
    cities_data = [
        {'name': 'Алматы'},
        {'name': 'Астана'},
        {'name': 'Шымкент'},
        {'name': 'Актобе'},
        {'name': 'Караганда'},
        {'name': 'Тараз'},
        {'name': 'Павлодар'},
        {'name': 'Семей'},
        {'name': 'Усть-Каменогорск'},
        {'name': 'Уральск'},
        {'name': 'Кызылорда'},
        {'name': 'Костанай'},
        {'name': 'Петропавловск'},
        {'name': 'Атырау'},
        {'name': 'Актау'},
        {'name': 'Темиртау'},
        {'name': 'Туркестан'},
        {'name': 'Кокшетау'},
        {'name': 'Талдыкорган'},
        {'name': 'Экибастуз'},
        {'name': 'Рудный'},
        {'name': 'Жанаозен'},
        {'name': 'Жезказган'},
        {'name': 'Балхаш'},
        {'name': 'Кентау'},
        {'name': 'Сатпаев'},
        {'name': 'Кайнар'},
        {'name': 'Арыс'},
        {'name': 'Лисаковск'},
        {'name': 'Риддер'},
        {'name': 'Степногорск'},
        {'name': 'Щучинск'},
        {'name': 'Зайсан'},
        {'name': 'Аксу'},
        {'name': 'Кандыагаш'},
        {'name': 'Житикара'},
        {'name': 'Каркаралинск'},
        {'name': 'Приозерск'},
        {'name': 'Курчатов'},
        {'name': 'Сарканд'},
        {'name': 'Аягоз'},
        {'name': 'Алга'},
        {'name': 'Шардара'},
        {'name': 'Жаркент'},
        {'name': 'Уштобе'},
        {'name': 'Текели'},
        {'name': 'Капчагай'},
        {'name': 'Талгар'},
        {'name': 'Есик'},
        {'name': 'Каскелен'},
        {'name': 'Шелек'},
        {'name': 'Жаркент'},
        {'name': 'Уштобе'},
        {'name': 'Текели'},
        {'name': 'Капчагай'},
        {'name': 'Талгар'},
        {'name': 'Есик'},
        {'name': 'Каскелен'},
        {'name': 'Шелек'},
    ]
    
    created_count = 0
    for data in cities_data:
        city, created = City.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            created_count += 1
            print(f"Создан город: {data['name']}")
        else:
            print(f"Город уже существует: {data['name']}")
    
    print(f"\nВсего создано новых городов: {created_count}")
    print(f"Всего городов в базе: {City.objects.count()}")

if __name__ == '__main__':
    add_cities() 