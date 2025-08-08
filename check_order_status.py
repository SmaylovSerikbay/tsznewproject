#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import Order, OrderResponse

def check_order_status(order_id):
    try:
        order = Order.objects.get(id=order_id)
        print(f"Заказ ID: {order.id}")
        print(f"Название: {order.title}")
        print(f"Статус: {order.status}")
        print(f"Тип заказа: {order.order_type}")
        print(f"Услуги: {order.services}")
        print(f"Выбранные исполнители: {order.selected_performers}")
        print(f"Создан: {order.created_at}")
        
        # Получаем все отклики на этот заказ
        responses = OrderResponse.objects.filter(order=order)
        print(f"\nОтклики на заказ ({responses.count()}):")
        for response in responses:
            print(f"  - Отклик {response.id}: {response.performer.get_full_name()} - {response.status}")
        
        return order
    except Order.DoesNotExist:
        print(f"Заказ с ID {order_id} не найден")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        order_id = int(sys.argv[1])
        check_order_status(order_id)
    else:
        print("Использование: python check_order_status.py <order_id>")
        print("Пример: python check_order_status.py 96")
