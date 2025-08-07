#!/usr/bin/env python3
"""
Скрипт для исправления структуры файлов на сервере
"""

import subprocess
import os

def fix_server_files():
    """Исправляет структуру файлов на сервере"""
    print("🔧 Исправляем структуру файлов на сервере...")
    
    # Команды для исправления
    commands = [
        # Создаем папку profile_photos если её нет
        "ssh root@77.246.247.137 'mkdir -p /root/tsznewproject/media/profile_photos'",
        
        # Перемещаем файлы профилей из portfolio в profile_photos
        "ssh root@77.246.247.137 'find /root/tsznewproject/media/portfolio -name \"*profile*\" -exec mv {} /root/tsznewproject/media/profile_photos/ \\;'",
        
        # Перемещаем файлы аватаров
        "ssh root@77.246.247.137 'find /root/tsznewproject/media/portfolio -name \"*avatar*\" -exec mv {} /root/tsznewproject/media/profile_photos/ \\;'",
        
        # Перемещаем файлы с префиксом user_ в profile_photos
        "ssh root@77.246.247.137 'find /root/tsznewproject/media/portfolio -name \"user_*\" -exec mv {} /root/tsznewproject/media/profile_photos/ \\;'",
        
        # Устанавливаем правильные права доступа
        "ssh root@77.246.247.137 'chmod -R 755 /root/tsznewproject/media'",
        "ssh root@77.246.247.137 'chown -R 1000:1000 /root/tsznewproject/media'",
        
        # Перезапускаем контейнеры
        "ssh root@77.246.247.137 'cd /root/tsznewproject && docker-compose restart'"
    ]
    
    for cmd in commands:
        print(f"\n📋 Выполняем: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Успешно")
            else:
                print(f"❌ Ошибка: {result.stderr}")
        except Exception as e:
            print(f"❌ Ошибка выполнения: {e}")
    
    print("\n✅ Исправление структуры файлов завершено!")

if __name__ == '__main__':
    fix_server_files()
