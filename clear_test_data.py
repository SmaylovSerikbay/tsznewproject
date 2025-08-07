#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Order, Portfolio, Tariff, BusyDate, Review, OrderResponse

def clear_test_data():
    print("🧹 Очистка тестовых данных...")
    
    # Удаляем тестовых пользователей
    test_users = User.objects.filter(
        username__startswith='test_') | User.objects.filter(
        username__startswith='performer_') | User.objects.filter(
        username__startswith='performer_catalog_')
    
    print(f"🗑️ Удаление {test_users.count()} тестовых пользователей...")
    test_users.delete()
    
    # Удаляем все заказы, портфолио, тарифы и т.д.
    print("🗑️ Удаление всех заказов...")
    Order.objects.all().delete()
    
    print("🗑️ Удаление всего портфолио...")
    Portfolio.objects.all().delete()
    
    print("🗑️ Удаление всех тарифов...")
    Tariff.objects.all().delete()
    
    print("🗑️ Удаление всех занятых дат...")
    BusyDate.objects.all().delete()
    
    print("🗑️ Удаление всех отзывов...")
    Review.objects.all().delete()
    
    print("🗑️ Удаление всех откликов...")
    OrderResponse.objects.all().delete()
    
    print("✅ База данных очищена от тестовых данных!")

if __name__ == '__main__':
    clear_test_data() 