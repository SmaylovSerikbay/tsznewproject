#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import Order, User, OrderResponse
from main.notifications import WhatsAppNotificationService

def test_notifications():
    """Тестирование системы уведомлений"""
    print("Тестирование системы WhatsApp уведомлений...")
    
    # Получаем тестовые данные
    try:
        # Получаем первый заказ
        order = Order.objects.filter(status='new').first()
        if not order:
            print("Нет заказов со статусом 'new' для тестирования")
            return
        
        # Получаем исполнителей
        performers = User.objects.filter(
            user_type='performer',
            is_active=True,
            is_phone_verified=True
        )[:3]  # Берем первых 3 для тестирования
        
        if not performers:
            print("Нет активных исполнителей с подтвержденными телефонами")
            return
        
        print(f"Тестируем с заказом: {order.title}")
        print(f"Найдено исполнителей: {performers.count()}")
        
        # Тестируем отправку уведомлений о новой заявке
        notification_service = WhatsAppNotificationService()
        
        print("\nОтправляем уведомления о новой заявке...")
        notification_service.send_new_order_notification(order, performers)
        
        print("Тестирование завершено!")
        
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")

if __name__ == "__main__":
    test_notifications()
