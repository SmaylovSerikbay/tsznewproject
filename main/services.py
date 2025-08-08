import requests
import random
import json
import re
from django.conf import settings

def normalize_phone_number(phone_number):
    """
    Нормализует номер телефона к формату +7XXXXXXXXXX
    Поддерживает форматы:
    - +77712641298
    - 87712641298
    - 77712641298
    - +7 771 264 12 98
    - 8 (771) 264-12-98
    """
    # Удаляем все символы кроме цифр
    digits_only = re.sub(r'[^\d]', '', phone_number)
    
    # Если номер начинается с 8, заменяем на 7
    if digits_only.startswith('8'):
        digits_only = '7' + digits_only[1:]
    
    # Если номер начинается с 7 и имеет 11 цифр, добавляем +
    if digits_only.startswith('7') and len(digits_only) == 11:
        return '+' + digits_only
    
    # Если номер уже в правильном формате (начинается с +7)
    if phone_number.startswith('+7'):
        # Удаляем все символы кроме цифр и добавляем +
        digits_only = re.sub(r'[^\d]', '', phone_number)
        if len(digits_only) == 11 and digits_only.startswith('7'):
            return '+' + digits_only
    
    # Если ничего не подошло, возвращаем исходный номер
    return phone_number

class WhatsAppOTPService:
    def __init__(self):
        # ЗАМЕНИТЕ НА ВАШИ РЕАЛЬНЫЕ ДАННЫЕ ОТ GREEN API
        self.base_url = "https://7105.api.greenapi.com"
        self.instance_id = "7105251898"  # Замените на ваш instance_id
        self.api_token = "53685780538a4b39a7deeb62cdabbbe5b64ddba9d4e44bcbb6"  # Замените на ваш api_token

    def generate_otp(self):
        """Generate a 6-digit OTP code"""
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    def send_otp(self, phone_number, otp_code):
        """Send OTP via WhatsApp using Green API"""
        endpoint = f"{self.base_url}/waInstance{self.instance_id}/sendMessage/{self.api_token}"
        
        # Нормализуем номер телефона
        normalized_phone = normalize_phone_number(phone_number)
        print(f'Original phone number: {phone_number}')
        print(f'Normalized phone number: {normalized_phone}')
        
        # Format phone number to WhatsApp format (remove + and spaces)
        whatsapp_number = normalized_phone.replace('+', '').replace(' ', '')
        print(f'WhatsApp formatted phone number: {whatsapp_number}')
        
        message = f"*Той со звездой*\n\nВаш код подтверждения: *{otp_code}*\n\nНикому не сообщайте этот код."
        print(f'Message to send: {message}')
        
        payload = {
            "chatId": f"{whatsapp_number}@c.us",
            "message": message
        }
        print(f'Payload: {payload}')
        print(f'Endpoint: {endpoint}')
        
        try:
            response = requests.post(endpoint, json=payload)
            print(f'Response status: {response.status_code}')
            print(f'Response content: {response.text}')
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending WhatsApp message: {e}")
            return False

    def verify_otp(self, phone_number, otp_code, stored_otp):
        """Verify the OTP code"""
        if not stored_otp.is_valid():
            return False
            
        stored_otp.attempts += 1
        stored_otp.save()
        
        if stored_otp.code == otp_code:
            stored_otp.is_verified = True
            stored_otp.save()
            return True
            
        return False 