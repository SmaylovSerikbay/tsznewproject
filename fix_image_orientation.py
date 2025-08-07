#!/usr/bin/env python3
"""
Скрипт для исправления ориентации изображений в портфолио
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import Portfolio
from PIL import Image, ImageOps
from django.core.files import File
import io

def fix_image_orientation():
    """Исправляет ориентацию всех изображений в портфолио"""
    print("🖼️ Исправляем ориентацию изображений...")
    
    # Получаем все изображения
    portfolio_items = Portfolio.objects.filter(media_type='image')
    print(f"📊 Найдено изображений: {portfolio_items.count()}")
    
    fixed_count = 0
    
    for item in portfolio_items:
        if not item.image:
            continue
            
        try:
            print(f"🔧 Обрабатываем: {item.image.name}")
            
            # Открываем изображение
            img = Image.open(item.image.path)
            
            # Проверяем, нужно ли поворачивать
            original_size = img.size
            
            # Автоматически поворачиваем согласно EXIF
            img = ImageOps.exif_transpose(img)
            
            # Если размер изменился, значит было повернуто
            if img.size != original_size:
                print(f"  ↻ Повернуто: {original_size} → {img.size}")
                
                # Конвертируем в RGB если нужно
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Сохраняем исправленное изображение
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Обновляем файл
                filename = os.path.basename(item.image.name)
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_fixed.jpg"
                item.image.save(new_filename, File(output), save=False)
                
                # Обновляем размер файла
                item.file_size = len(output.getvalue())
                item.save()
                
                fixed_count += 1
                print(f"  ✅ Исправлено")
            else:
                print(f"  ✓ Ориентация правильная")
                
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    print(f"\n✅ Исправлено изображений: {fixed_count}")

if __name__ == '__main__':
    fix_image_orientation()
