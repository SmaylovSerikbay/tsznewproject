#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import Order, User

def check_active_orders():
    # Получаем все заказы в работе
    in_progress_orders = Order.objects.filter(status='in_progress')
    print(f"Заказы в работе: {in_progress_orders.count()}")
    
    for order in in_progress_orders:
        print(f"\nЗаказ ID: {order.id}")
        print(f"Название: {order.title}")
        print(f"Статус: {order.status}")
        print(f"Тип заказа: {order.order_type}")
        print(f"Заказчик: {order.customer.get_full_name()}")
        print(f"Исполнитель: {order.performer.get_full_name() if order.performer else 'Не назначен'}")
        print(f"Выбранные исполнители: {order.selected_performers}")
        print(f"Дата события: {order.event_date}")
    
    # Получаем всех исполнителей
    performers = User.objects.filter(user_type='performer')
    print(f"\nИсполнители ({performers.count()}):")
    for performer in performers[:5]:  # Показываем первых 5
        print(f"  - {performer.get_full_name()} (ID: {performer.id})")

if __name__ == "__main__":
    check_active_orders()
