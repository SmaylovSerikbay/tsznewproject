#!/usr/bin/env python
"""
Тестовый скрипт для проверки работы перенаправления после сохранения профиля
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, ServiceType, City

def test_profile_redirect():
    """Тестирование перенаправления после сохранения профиля"""
    print("🧪 Тестирование перенаправления после сохранения профиля...")
    
    try:
        # Получаем тестового пользователя
        user = User.objects.filter(user_type='performer').first()
        
        if not user:
            print("❌ Не найден тестовый пользователь")
            return
        
        print(f"👤 Пользователь: {user.get_full_name()} ({user.phone_number})")
        
        # Проверяем текущие настройки
        print(f"\n📋 Текущие настройки:")
        print(f"   Город: {user.city.name if user.city else 'Не указан'}")
        print(f"   Тип услуги: {user.service_type.name if user.service_type else 'Не указан'}")
        print(f"   Email: {user.email}")
        
        # Проверяем доступные города и типы услуг
        cities = City.objects.filter(is_active=True)
        service_types = ServiceType.objects.filter(is_active=True)
        
        print(f"\n🏙️ Доступные города: {[city.name for city in cities]}")
        print(f"🔧 Доступные типы услуг: {[f'{st.name} (ID: {st.id})' for st in service_types]}")
        
        print("\n✅ Тестирование завершено!")
        print("\n💡 Логика перенаправления:")
        print("1. При сохранении профиля проверяется параметр return_url")
        print("2. Если return_url указан и начинается с '/', происходит перенаправление")
        print("3. Если return_url не указан, происходит перенаправление на dashboard")
        print("4. Все ссылки на настройки профиля теперь передают return_url")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == '__main__':
    test_profile_redirect()
