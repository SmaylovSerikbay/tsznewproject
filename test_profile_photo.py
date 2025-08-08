#!/usr/bin/env python
"""
Тестовый скрипт для проверки работы фото профиля
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User

def test_profile_photo():
    """Тестирование работы фото профиля"""
    print("🧪 Тестирование работы фото профиля...")
    
    try:
        # Получаем тестовых пользователей
        customer = User.objects.filter(user_type='customer').first()
        performer = User.objects.filter(user_type='performer').first()
        
        if not customer or not performer:
            print("❌ Не найдены тестовые пользователи")
            return
        
        print(f"👤 Заказчик: {customer.get_full_name()}")
        print(f"   Фото профиля: {'Есть' if customer.profile_photo else 'Нет'}")
        if customer.profile_photo:
            print(f"   URL фото: {customer.profile_photo.url}")
        
        print(f"\n🎭 Исполнитель: {performer.get_full_name()}")
        print(f"   Фото профиля: {'Есть' if performer.profile_photo else 'Нет'}")
        if performer.profile_photo:
            print(f"   URL фото: {performer.profile_photo.url}")
        
        print("\n✅ Тестирование завершено!")
        print("\n💡 Проверьте:")
        print("1. Открытие модального окна редактирования профиля")
        print("2. Отображение текущего фото в модальном окне")
        print("3. Предварительный просмотр при выборе нового фото")
        print("4. Сохранение нового фото")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == '__main__':
    test_profile_photo()
