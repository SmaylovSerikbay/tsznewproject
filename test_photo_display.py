#!/usr/bin/env python
"""
Тестовый скрипт для проверки отображения фото профиля
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User

def test_photo_display():
    """Тестирование отображения фото профиля"""
    print("🧪 Тестирование отображения фото профиля...")
    
    try:
        # Получаем пользователей с фото
        users_with_photo = User.objects.filter(profile_photo__isnull=False)
        users_without_photo = User.objects.filter(profile_photo__isnull=True)
        
        print(f"👥 Пользователей с фото: {users_with_photo.count()}")
        print(f"👥 Пользователей без фото: {users_without_photo.count()}")
        
        if users_with_photo.exists():
            user = users_with_photo.first()
            print(f"\n✅ Пример пользователя с фото:")
            print(f"   Имя: {user.get_full_name()}")
            print(f"   Фото: {user.profile_photo.name}")
            print(f"   URL: {user.profile_photo.url}")
            print(f"   Размер: {user.profile_photo.size} байт")
        
        if users_without_photo.exists():
            user = users_without_photo.first()
            print(f"\n❌ Пример пользователя без фото:")
            print(f"   Имя: {user.get_full_name()}")
            print(f"   Фото: Не установлено")
        
        print("\n✅ Тестирование завершено!")
        print("\n💡 Проверьте в браузере:")
        print("1. Откройте модальное окно редактирования профиля")
        print("2. Убедитесь, что текущее фото отображается")
        print("3. Попробуйте выбрать новое фото")
        print("4. Проверьте предварительный просмотр")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == '__main__':
    test_photo_display()
