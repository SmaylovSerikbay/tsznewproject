#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import OrderResponse

def check_response_status(response_id):
    try:
        response = OrderResponse.objects.get(id=response_id)
        print(f"Отклик ID: {response.id}")
        print(f"Статус: {response.status}")
        print(f"Заказ: {response.order.id}")
        print(f"Исполнитель: {response.performer.get_full_name()}")
        print(f"Создан: {response.created_at}")
        return response
    except OrderResponse.DoesNotExist:
        print(f"Отклик с ID {response_id} не найден")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        response_id = int(sys.argv[1])
        check_response_status(response_id)
    else:
        print("Использование: python check_response_status.py <response_id>")
        print("Пример: python check_response_status.py 22")
