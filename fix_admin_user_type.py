#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User

def fix_admin_user_type():
    """Исправляет user_type для админов"""
    # Находим всех суперпользователей
    admins = User.objects.filter(is_superuser=True)
    
    fixed_count = 0
    for admin in admins:
        if not admin.user_type or admin.user_type not in ['customer', 'performer']:
            # Устанавливаем user_type как 'customer' для админов
            admin.user_type = 'customer'
            admin.save()
            print(f"Исправлен админ {admin.username}: user_type = {admin.user_type}")
            fixed_count += 1
        else:
            print(f"Админ {admin.username} уже имеет правильный user_type: {admin.user_type}")
    
    print(f"\nВсего исправлено админов: {fixed_count}")
    print(f"Всего админов в базе: {admins.count()}")

if __name__ == '__main__':
    fix_admin_user_type() 