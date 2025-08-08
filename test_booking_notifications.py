#!/usr/bin/env python
"""
Тестовый скрипт для проверки уведомлений бронирования
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Order, Tariff, ServiceType, City
from main.notifications import WhatsAppNotificationService
from datetime import date, timedelta

def test_booking_notifications():
    """Тестирование уведомлений бронирования"""
    print("🧪 Тестирование уведомлений бронирования...")
    
    # Получаем тестовых пользователей
    try:
        customer = User.objects.filter(user_type='customer').first()
        performer = User.objects.filter(user_type='performer').first()
        
        if not customer or not performer:
            print("❌ Не найдены тестовые пользователи (заказчик и исполнитель)")
            return
        
        print(f"👤 Заказчик: {customer.get_full_name()} ({customer.phone_number})")
        print(f"🎭 Исполнитель: {performer.get_full_name()} ({performer.phone_number})")
        
        # Создаем тестовый тариф
        tariff, created = Tariff.objects.get_or_create(
            user=performer,
            defaults={
                'name': 'Тестовый тариф',
                'price': 50000,
                'description': 'Тестовый тариф для проверки уведомлений'
            }
        )
        
        # Создаем тестовый заказ-бронирование
        test_date = date.today() + timedelta(days=7)
        order = Order.objects.create(
            customer=customer,
            performer=performer,
            title='Тестовое бронирование',
            event_type='other',
            event_date=test_date,
            city='Алматы',
            venue='Тестовое место',
            guest_count=10,
            description='Тестовое описание бронирования',
            budget=tariff.price,
            services=[],
            tariff=tariff,
            details='Тестовые детали бронирования',
            order_type='booking',
            status='new'
        )
        
        print(f"📋 Создан тестовый заказ: {order.title}")
        
        # Инициализируем сервис уведомлений
        notification_service = WhatsAppNotificationService()
        
        # Тестируем уведомление о новом бронировании
        print("\n📞 Тестирование уведомления о новом бронировании...")
        try:
            notification_service.send_new_booking_notification(order)
            print("✅ Уведомление о новом бронировании отправлено")
        except Exception as e:
            print(f"❌ Ошибка при отправке уведомления о новом бронировании: {e}")
        
        # Тестируем уведомление о принятии бронирования
        print("\n✅ Тестирование уведомления о принятии бронирования...")
        try:
            notification_service.send_booking_accepted_notification(order)
            print("✅ Уведомление о принятии бронирования отправлено")
        except Exception as e:
            print(f"❌ Ошибка при отправке уведомления о принятии бронирования: {e}")
        
        # Тестируем уведомление об отклонении бронирования
        print("\n❌ Тестирование уведомления об отклонении бронирования...")
        try:
            notification_service.send_booking_rejected_notification(order)
            print("✅ Уведомление об отклонении бронирования отправлено")
        except Exception as e:
            print(f"❌ Ошибка при отправке уведомления об отклонении бронирования: {e}")
        
        # Тестируем уведомление об отмене бронирования исполнителем
        print("\n🚫 Тестирование уведомления об отмене бронирования исполнителем...")
        try:
            notification_service.send_booking_cancelled_by_performer_notification(order)
            print("✅ Уведомление об отмене бронирования исполнителем отправлено")
        except Exception as e:
            print(f"❌ Ошибка при отправке уведомления об отмене бронирования исполнителем: {e}")
        
        # Тестируем уведомление об отмене бронирования заказчиком
        print("\n🚫 Тестирование уведомления об отмене бронирования заказчиком...")
        try:
            notification_service.send_booking_cancelled_by_customer_notification(order)
            print("✅ Уведомление об отмене бронирования заказчиком отправлено")
        except Exception as e:
            print(f"❌ Ошибка при отправке уведомления об отмене бронирования заказчиком: {e}")
        
        # Удаляем тестовый заказ
        order.delete()
        print(f"\n🗑️ Тестовый заказ удален")
        
        print("\n🎉 Тестирование завершено!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == '__main__':
    test_booking_notifications()
