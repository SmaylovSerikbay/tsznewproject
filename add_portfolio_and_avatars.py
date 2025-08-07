#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime
from decimal import Decimal
import requests
from io import BytesIO
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

def add_portfolio_and_avatars():
    print("Добавление портфолио и аватаров...")
    
    # Получаем пользователей
    customer = User.objects.get(username='customer_test')
    photographer = User.objects.get(username='photographer_test')
    host = User.objects.get(username='host_test')
    musician = User.objects.get(username='musician_test')
    
    # Аватары для пользователей (используем placeholder изображения)
    avatar_urls = {
        'customer_test': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&crop=face',
        'photographer_test': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=200&h=200&fit=crop&crop=face',
        'host_test': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face',
        'musician_test': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&h=200&fit=crop&crop=face'
    }
    
    # Добавляем аватары
    for username, avatar_url in avatar_urls.items():
        user = User.objects.get(username=username)
        avatar_file = download_image(avatar_url, f'{username}_avatar.jpg')
        if avatar_file:
            user.profile_photo.save(f'{username}_avatar.jpg', avatar_file, save=True)
            print(f"✅ Добавлен аватар для {user.get_full_name()}")
    
    # Портфолио для фотографа
    photographer_portfolio_urls = [
        'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1519741497674-611481863552?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1519741497674-611481863552?w=400&h=300&fit=crop'
    ]
    
    for i, url in enumerate(photographer_portfolio_urls):
        portfolio_file = download_image(url, f'photographer_portfolio_{i+1}.jpg')
        if portfolio_file:
            Portfolio.objects.create(
                user=photographer,
                image=portfolio_file
            )
            print(f"✅ Добавлено фото {i+1} в портфолио фотографа")
    
    # Портфолио для ведущего (фото с мероприятий)
    host_portfolio_urls = [
        'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1519741497674-611481863552?w=400&h=300&fit=crop'
    ]
    
    for i, url in enumerate(host_portfolio_urls):
        portfolio_file = download_image(url, f'host_portfolio_{i+1}.jpg')
        if portfolio_file:
            Portfolio.objects.create(
                user=host,
                image=portfolio_file
            )
            print(f"✅ Добавлено фото {i+1} в портфолио ведущего")
    
    # Портфолио для музыканта (фото с выступлений)
    musician_portfolio_urls = [
        'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=400&h=300&fit=crop'
    ]
    
    for i, url in enumerate(musician_portfolio_urls):
        portfolio_file = download_image(url, f'musician_portfolio_{i+1}.jpg')
        if portfolio_file:
            Portfolio.objects.create(
                user=musician,
                image=portfolio_file
            )
            print(f"✅ Добавлено фото {i+1} в портфолио музыканта")
    
    # Портфолио для заказчика (фото с его мероприятий)
    customer_portfolio_urls = [
        'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1519741497674-611481863552?w=400&h=300&fit=crop'
    ]
    
    for i, url in enumerate(customer_portfolio_urls):
        portfolio_file = download_image(url, f'customer_portfolio_{i+1}.jpg')
        if portfolio_file:
            Portfolio.objects.create(
                user=customer,
                image=portfolio_file
            )
            print(f"✅ Добавлено фото {i+1} в портфолио заказчика")
    
    print("\n" + "="*50)
    print("🎉 ПОРТФОЛИО И АВАТАРЫ ДОБАВЛЕНЫ!")
    print("="*50)
    
    # Статистика
    total_portfolio = Portfolio.objects.count()
    users_with_avatars = User.objects.exclude(profile_photo='').count()
    
    print(f"\n📊 СТАТИСТИКА:")
    print(f"   Всего фото в портфолио: {total_portfolio}")
    print(f"   Пользователей с аватарами: {users_with_avatars}")
    
    print(f"\n📸 ПОРТФОЛИО ПО ПОЛЬЗОВАТЕЛЯМ:")
    print(f"   Фотограф: {Portfolio.objects.filter(user=photographer).count()} фото")
    print(f"   Ведущий: {Portfolio.objects.filter(user=host).count()} фото")
    print(f"   Музыкант: {Portfolio.objects.filter(user=musician).count()} фото")
    print(f"   Заказчик: {Portfolio.objects.filter(user=customer).count()} фото")
    
    print(f"\n🌐 ССЫЛКА НА САЙТ:")
    print("   http://localhost:8000")
    
    print("\n" + "="*50)

if __name__ == '__main__':
    add_portfolio_and_avatars() 