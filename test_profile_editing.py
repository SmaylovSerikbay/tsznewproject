#!/usr/bin/env python
"""
Тестовый скрипт для проверки работы редактирования профиля
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, ServiceType, City

def test_profile_editing():
    """Тестирование редактирования профиля"""
    print("🧪 Тестирование редактирования профиля...")
    
    # Получаем тестовых пользователей
    try:
        customer = User.objects.filter(user_type='customer').first()
        performer = User.objects.filter(user_type='performer').first()
        
        if not customer or not performer:
            print("❌ Не найдены тестовые пользователи (заказчик и исполнитель)")
            return
        
        print(f"👤 Заказчик: {customer.get_full_name()} ({customer.phone_number})")
        print(f"🎭 Исполнитель: {performer.get_full_name()} ({performer.phone_number})")
        
        # Проверяем города
        cities = City.objects.filter(is_active=True)
        print(f"🏙️ Доступные города: {[city.name for city in cities]}")
        
        # Проверяем типы услуг
        service_types = ServiceType.objects.filter(is_active=True)
        print(f"🔧 Доступные типы услуг: {[f'{st.name} (ID: {st.id})' for st in service_types]}")
        
        # Проверяем текущие настройки пользователей
        print(f"\n📋 Текущие настройки заказчика:")
        print(f"   Город: {customer.city.name if customer.city else 'Не указан'}")
        print(f"   Email: {customer.email}")
        
        print(f"\n📋 Текущие настройки исполнителя:")
        print(f"   Город: {performer.city.name if performer.city else 'Не указан'}")
        print(f"   Тип услуги: {performer.service_type.name if performer.service_type else 'Не указан'}")
        print(f"   Email: {performer.email}")
        
        print("\n✅ Тестирование завершено!")
        print("\n💡 Рекомендации:")
        print("1. Убедитесь, что в базе данных есть города и типы услуг")
        print("2. Проверьте, что пользователи имеют корректные данные")
        print("3. При редактировании профиля используйте существующие города и типы услуг")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == '__main__':
    test_profile_editing()
