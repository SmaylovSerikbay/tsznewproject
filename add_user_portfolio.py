#!/usr/bin/env python
import os
import sys
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, Portfolio

def add_user_portfolio():
    print("📸 Добавление фотографий в портфолио пользователя +77085446945...")
    
    # Находим пользователя
    user = User.objects.filter(phone_number='+77085446945').first()
    if not user:
        print("❌ Пользователь с номером +77085446945 не найден!")
        return
    
    print(f"✅ Найден пользователь: {user.get_full_name()}")
    
    # Проверяем, есть ли фотографии в папке media/portfolio
    portfolio_dir = 'media/portfolio'
    if not os.path.exists(portfolio_dir):
        print(f"❌ Папка {portfolio_dir} не существует!")
        return
    
    # Получаем список файлов в папке portfolio
    portfolio_files = []
    for filename in os.listdir(portfolio_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            portfolio_files.append(filename)
    
    if not portfolio_files:
        print("❌ В папке portfolio нет изображений!")
        return
    
    print(f"📁 Найдено {len(portfolio_files)} изображений в папке portfolio")
    
    # Удаляем существующие записи портфолио
    Portfolio.objects.filter(user=user).delete()
    
    # Создаем записи портфолио для каждого изображения
    for i, filename in enumerate(portfolio_files[:15]):  # Максимум 15 фотографий
        file_path = f'portfolio/{filename}'
        try:
            Portfolio.objects.create(
                user=user,
                image=file_path
            )
            print(f"✅ Добавлена фотография: {filename}")
        except Exception as e:
            print(f"❌ Ошибка при добавлении {filename}: {e}")
    
    print(f"\n🎉 В портфолио добавлено {Portfolio.objects.filter(user=user).count()} фотографий!")

if __name__ == '__main__':
    add_user_portfolio() 