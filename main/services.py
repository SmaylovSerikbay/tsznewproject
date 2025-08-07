import requests
import random
import json
from django.conf import settings

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
        
        # Format phone number to WhatsApp format (remove + and spaces)
        whatsapp_number = phone_number.replace('+', '').replace(' ', '')
        print(f'Formatted phone number: {whatsapp_number}')
        
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