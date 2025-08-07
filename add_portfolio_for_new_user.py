#!/usr/bin/env python
import os
import sys
import django
import requests
from django.core.files.base import ContentFile

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Portfolio

def download_image(url, filename):
    """Загружает изображение по URL и возвращает ContentFile"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return ContentFile(response.content, name=filename)
    except Exception as e:
        print(f"Ошибка загрузки изображения {url}: {e}")
        return None

def add_portfolio_for_new_user():
    print("Добавление портфолио и аватара для нового исполнителя...")
    
    # Получаем нового исполнителя
    performer = User.objects.get(username='performer_user')
    
    # Добавляем аватар
    avatar_url = 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face'
    avatar_file = download_image(avatar_url, 'performer_user_avatar.jpg')
    if avatar_file:
        performer.profile_photo.save('performer_user_avatar.jpg', avatar_file, save=True)
        print(f"✅ Добавлен аватар для {performer.get_full_name()}")
    
    # Портфолио для нового исполнителя
    portfolio_urls = [
        'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1519741497674-611481863552?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400&h=300&fit=crop'
    ]
    
    for i, url in enumerate(portfolio_urls):
        portfolio_file = download_image(url, f'performer_user_portfolio_{i+1}.jpg')
        if portfolio_file:
            Portfolio.objects.create(
                user=performer,
                image=portfolio_file
            )
            print(f"✅ Добавлено фото {i+1} в портфолио исполнителя")
    
    print("\n" + "="*50)
    print("🎉 ПОРТФОЛИО ДОБАВЛЕНО!")
    print("="*50)
    
    # Статистика
    portfolio_count = Portfolio.objects.filter(user=performer).count()
    print(f"\n📊 СТАТИСТИКА:")
    print(f"   Фото в портфолио: {portfolio_count}")
    print(f"   Аватар: {'✅' if performer.profile_photo else '❌'}")
    
    print(f"\n🌐 ССЫЛКА НА САЙТ:")
    print("   http://localhost:8000")
    
    print("\n" + "="*50)

if __name__ == '__main__':
    add_portfolio_for_new_user() 