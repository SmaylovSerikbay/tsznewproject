#!/usr/bin/env python
import os
import sys
import django
import requests
from django.core.files.base import ContentFile

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User

def fix_photographer_avatar():
    print("Исправление аватара фотографа...")
    
    photographer = User.objects.get(username='photographer_test')
    
    # Альтернативный URL для аватара фотографа
    avatar_url = 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&h=200&fit=crop&crop=face'
    
    try:
        response = requests.get(avatar_url, timeout=10)
        response.raise_for_status()
        avatar_file = ContentFile(response.content, name='photographer_avatar_fixed.jpg')
        photographer.profile_photo.save('photographer_avatar_fixed.jpg', avatar_file, save=True)
        print(f"✅ Аватар исправлен для {photographer.get_full_name()}")
    except Exception as e:
        print(f"❌ Ошибка загрузки аватара: {e}")
    
    # Проверяем статистику
    users_with_avatars = User.objects.exclude(profile_photo='').count()
    print(f"\n📊 Обновленная статистика:")
    print(f"   Пользователей с аватарами: {users_with_avatars}")

if __name__ == '__main__':
    fix_photographer_avatar() 