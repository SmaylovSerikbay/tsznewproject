#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import ServiceType

def add_service_types():
    """Добавляет типы услуг в базу данных"""
    
    service_types_data = [
        {
            'code': 'photo',
            'name': 'Фотографы',
            'description': 'Профессиональная фотосъемка мероприятий',
            'icon': 'ri-camera-line',
            'sort_order': 1
        },
        {
            'code': 'video',
            'name': 'Видеографы',
            'description': 'Видеосъемка и монтаж видео',
            'icon': 'ri-video-line',
            'sort_order': 2
        },
        {
            'code': 'music',
            'name': 'Музыканты',
            'description': 'Живая музыка и музыкальное сопровождение',
            'icon': 'ri-music-line',
            'sort_order': 3
        },
        {
            'code': 'host',
            'name': 'Ведущие',
            'description': 'Ведущие мероприятий и тамады',
            'icon': 'ri-user-voice-line',
            'sort_order': 4
        },
        {
            'code': 'dance',
            'name': 'Шоу-программы',
            'description': 'Танцевальные и развлекательные программы',
            'icon': 'ri-dance-line',
            'sort_order': 5
        },
        {
            'code': 'restaurant',
            'name': 'Рестораны',
            'description': 'Рестораны и кейтеринг',
            'icon': 'ri-restaurant-line',
            'sort_order': 6
        },
        {
            'code': 'makeup',
            'name': 'Визожисты',
            'description': 'Макияж и стилисты',
            'icon': 'ri-magic-line',
            'sort_order': 7
        },
        {
            'code': 'registry',
            'name': 'Регистрация брака',
            'description': 'Организация регистрации брака',
            'icon': 'ri-heart-line',
            'sort_order': 8
        },
        {
            'code': 'cottage',
            'name': 'Коттеджы',
            'description': 'Аренда коттеджей и загородных домов',
            'icon': 'ri-home-line',
            'sort_order': 9
        },
        {
            'code': 'recreation_areas',
            'name': 'Зоны отдыха',
            'description': 'Зоны отдыха и развлечений',
            'icon': 'ri-map-pin-line',
            'sort_order': 10
        },
        {
            'code': 'star',
            'name': 'Звезды Эстрады',
            'description': 'Известные артисты и звезды',
            'icon': 'ri-star-line',
            'sort_order': 11
        },
        {
            'code': 'aphishe',
            'name': 'Концертные Афишы',
            'description': 'Концерты и шоу-программы',
            'icon': 'ri-calendar-event-line',
            'sort_order': 12
        }
    ]
    
    created_count = 0
    for data in service_types_data:
        service_type, created = ServiceType.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        if created:
            created_count += 1
            print(f"Создан тип услуги: {data['name']}")
        else:
            print(f"Тип услуги уже существует: {data['name']}")
    
    print(f"\nВсего создано новых типов услуг: {created_count}")
    print(f"Всего типов услуг в базе: {ServiceType.objects.count()}")

if __name__ == '__main__':
    add_service_types() 