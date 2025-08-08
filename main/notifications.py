import requests
import json
from django.conf import settings
from .services import WhatsAppOTPService

class WhatsAppNotificationService:
    def __init__(self):
        # Используем существующий сервис для отправки OTP
        self.whatsapp_service = WhatsAppOTPService()
        self.base_url = self.whatsapp_service.base_url
        self.instance_id = self.whatsapp_service.instance_id
        self.api_token = self.whatsapp_service.api_token

    def send_notification(self, phone_number, message):
        """Отправка уведомления через WhatsApp"""
        endpoint = f"{self.base_url}/waInstance{self.instance_id}/sendMessage/{self.api_token}"
        
        # Форматируем номер телефона
        whatsapp_number = phone_number.replace('+', '').replace(' ', '')
        
        payload = {
            "chatId": f"{whatsapp_number}@c.us",
            "message": message
        }
        
        try:
            response = requests.post(endpoint, json=payload)
            print(f'WhatsApp notification sent to {phone_number}: {response.status_code}')
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending WhatsApp notification: {e}")
            return False

    def send_response_notification(self, response):
        """Уведомление о новом отклике"""
        order = response.order
        performer = response.performer
        customer = order.customer
        
        # Уведомление заказчику
        customer_message = f"""🎉 *Новый отклик на вашу заявку!*

📋 *Заявка:* {order.title}
👤 *Исполнитель:* {performer.get_full_name()}
💰 *Цена:* {response.price} ₸
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

💬 *Сообщение исполнителя:*
{response.message if response.message else 'Сообщение не указано'}

🔗 *Проверьте отклик:* https://toisozvezdoi.kz/auth/

_Ответьте на это сообщение, если у вас есть вопросы._"""
        
        if customer.phone_number:
            self.send_notification(customer.phone_number, customer_message)

    def send_response_accepted_notification(self, response):
        """Уведомление о принятии отклика"""
        order = response.order
        performer = response.performer
        customer = order.customer
        
        # Уведомление исполнителю
        performer_message = f"""✅ *Ваш отклик принят!*

📋 *Заявка:* {order.title}
👤 *Заказчик:* {customer.get_full_name()}
💰 *Цена:* {response.price} ₸
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

🎯 *Статус:* Заказ переведен в работу

🔗 *Просмотреть заказ:* https://toisozvezdoi.kz/auth/

_Свяжитесь с заказчиком для уточнения деталей._"""
        
        if performer.phone_number:
            self.send_notification(performer.phone_number, performer_message)

    def send_response_rejected_notification(self, response):
        """Уведомление об отклонении отклика"""
        order = response.order
        performer = response.performer
        
        # Уведомление исполнителю
        performer_message = f"""❌ *Отклик отклонен*

📋 *Заявка:* {order.title}
💰 *Ваша цена:* {response.price} ₸
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

😔 *К сожалению, заказчик выбрал другого исполнителя.*

🔗 *Найти другие заявки:* https://toisozvezdoi.kz/auth/

_Не расстраивайтесь, у вас еще много возможностей!_"""
        
        if performer.phone_number:
            self.send_notification(performer.phone_number, performer_message)

    def send_order_completed_notification(self, order):
        """Уведомление о завершении заказа"""
        performer = order.performer
        customer = order.customer
        
        # Уведомление исполнителю
        performer_message = f"""🎉 *Заказ завершен!*

📋 *Заявка:* {order.title}
👤 *Заказчик:* {customer.get_full_name() if customer else 'Не указан'}
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

✅ *Статус:* Заказ успешно выполнен

🔗 *Просмотреть заказ:* https://toisozvezdoi.kz/auth/

_Спасибо за качественную работу!_"""
        
        # Уведомление заказчику
        customer_message = f"""🎉 *Заказ завершен!*

📋 *Заявка:* {order.title}
👤 *Исполнитель:* {performer.get_full_name() if performer else 'Не указан'}
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

✅ *Статус:* Заказ успешно выполнен

🔗 *Просмотреть заказ:* https://toisozvezdoi.kz/auth/

_Не забудьте оставить отзыв исполнителю!_"""
        
        if performer and performer.phone_number:
            self.send_notification(performer.phone_number, performer_message)
        
        if customer.phone_number:
            self.send_notification(customer.phone_number, customer_message)

    def send_order_cancelled_notification(self, order, cancelled_by):
        """Уведомление об отмене заказа"""
        performer = order.performer
        customer = order.customer
        
        cancelled_by_name = cancelled_by.get_full_name()
        
        # Уведомление исполнителю
        if performer and performer != cancelled_by:
            performer_message = f"""❌ *Заказ отменен*

📋 *Заявка:* {order.title}
👤 *Отменил:* {cancelled_by_name}
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

😔 *Заказ был отменен.*

🔗 *Найти другие заявки:* https://toisozvezdoi.kz/auth/

_Не расстраивайтесь, у вас еще много возможностей!_"""
            
            if performer.phone_number:
                self.send_notification(performer.phone_number, performer_message)
        
        # Уведомление заказчику
        if customer != cancelled_by:
            customer_message = f"""❌ *Заказ отменен*

📋 *Заявка:* {order.title}
👤 *Отменил:* {cancelled_by_name}
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

😔 *Заказ был отменен.*

🔗 *Создать новую заявку:* https://toisozvezdoi.kz/auth/

_Вы можете создать новую заявку в любое время._"""
            
            if customer.phone_number:
                self.send_notification(customer.phone_number, customer_message)

    def send_response_cancelled_notification(self, response):
        """Уведомление об отмене отклика"""
        order = response.order
        performer = response.performer
        customer = order.customer
        
        # Уведомление заказчику
        customer_message = f"""🔄 *Отклик отменен*

📋 *Заявка:* {order.title}
👤 *Исполнитель:* {performer.get_full_name()}
💰 *Цена:* {response.price} ₸

😔 *Исполнитель отменил свой отклик.*

🔗 *Проверить другие отклики:* https://toisozvezdoi.kz/auth/

_Не волнуйтесь, у вас могут быть другие отклики._"""
        
        if customer.phone_number:
            self.send_notification(customer.phone_number, customer_message)

    def send_new_order_notification(self, order, performers):
        """Уведомление исполнителям о новой заявке"""
        for performer in performers:
            if not performer.phone_number:
                continue
                
            # Проверяем, подходит ли исполнитель для этой заявки
            if not performer.service_type:
                continue
                
            services = order.services or []
            if performer.service_type.code not in services:
                continue
            
            # Формируем сообщение для исполнителя
            performer_message = f"""🎯 *Новая заявка для вас!*

📋 *Заявка:* {order.title}
👤 *Заказчик:* {order.customer.get_full_name()}
💰 *Бюджет:* {order.budget} ₸
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}
📍 *Город:* {order.city}
👥 *Количество гостей:* {order.guest_count}

🎭 *Тип события:* {order.get_event_type_display()}
🔧 *Нужные услуги:* {', '.join(services)}

📝 *Описание:*
{order.description if order.description else 'Описание не указано'}

🔗 *Откликнуться:* https://toisozvezdoi.kz/auth/

_Не упустите возможность! Откликнитесь прямо сейчас._"""
            
            self.send_notification(performer.phone_number, performer_message)

    def send_new_booking_notification(self, order):
        """Уведомление исполнителю о новом бронировании"""
        performer = order.performer
        customer = order.customer
        
        # Уведомление исполнителю
        performer_message = f"""📞 *Новое бронирование!*

📋 *Заявка:* {order.title}
👤 *Заказчик:* {customer.get_full_name()}
💰 *Бюджет:* {order.budget} ₸
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}
📍 *Город:* {order.city}

📝 *Детали:*
{order.details if order.details else 'Детали не указаны'}

🔗 *Принять/Отклонить:* https://toisozvezdoi.kz/auth/

_Пожалуйста, ответьте на бронирование в течение 24 часов._"""
        
        if performer.phone_number:
            self.send_notification(performer.phone_number, performer_message)

    def send_booking_accepted_notification(self, order):
        """Уведомление о принятии бронирования"""
        performer = order.performer
        customer = order.customer
        
        # Уведомление заказчику
        customer_message = f"""✅ *Бронирование принято!*

📋 *Заявка:* {order.title}
👤 *Исполнитель:* {performer.get_full_name() if performer else 'Не указан'}
💰 *Бюджет:* {order.budget} ₸
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

🎯 *Статус:* Бронирование подтверждено

🔗 *Просмотреть заказ:* https://toisozvezdoi.kz/auth/

_Исполнитель готов к работе!_"""
        
        if customer.phone_number:
            self.send_notification(customer.phone_number, customer_message)

    def send_booking_rejected_notification(self, order):
        """Уведомление об отклонении бронирования"""
        performer = order.performer
        customer = order.customer
        
        # Уведомление заказчику
        customer_message = f"""❌ *Бронирование отклонено*

📋 *Заявка:* {order.title}
👤 *Исполнитель:* {performer.get_full_name() if performer else 'Не указан'}
💰 *Бюджет:* {order.budget} ₸
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

😔 *Исполнитель отклонил ваше бронирование.*

🔗 *Найти других исполнителей:* https://toisozvezdoi.kz/auth/

_Не расстраивайтесь, у вас еще много вариантов!_"""
        
        if customer.phone_number:
            self.send_notification(customer.phone_number, customer_message)

    def send_booking_cancelled_by_performer_notification(self, order):
        """Уведомление об отмене бронирования исполнителем"""
        performer = order.performer
        customer = order.customer
        
        # Уведомление заказчику
        customer_message = f"""❌ *Бронирование отменено*

📋 *Заявка:* {order.title}
👤 *Исполнитель:* {performer.get_full_name() if performer else 'Не указан'}
💰 *Бюджет:* {order.budget} ₸
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

😔 *Исполнитель отменил бронирование.*

🔗 *Найти других исполнителей:* https://toisozvezdoi.kz/auth/

_Не расстраивайтесь, у вас еще много вариантов!_"""
        
        if customer.phone_number:
            self.send_notification(customer.phone_number, customer_message)

    def send_booking_cancelled_by_customer_notification(self, order):
        """Уведомление об отмене бронирования заказчиком"""
        performer = order.performer
        customer = order.customer
        
        # Уведомление исполнителю
        performer_message = f"""❌ *Бронирование отменено*

📋 *Заявка:* {order.title}
👤 *Заказчик:* {customer.get_full_name()}
💰 *Бюджет:* {order.budget} ₸
📅 *Дата события:* {order.event_date.strftime('%d.%m.%Y')}

😔 *Заказчик отменил бронирование.*

🔗 *Найти другие заявки:* https://toisozvezdoi.kz/auth/

_Не расстраивайтесь, у вас еще много возможностей!_"""
        
        if performer.phone_number:
            self.send_notification(performer.phone_number, performer_message)
