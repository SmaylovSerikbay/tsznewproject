#!/usr/bin/env python3
"""
Скрипт для перезапуска контейнеров с правильными медиа файлами
"""

import subprocess

def restart_with_media():
    """Перезапускает контейнеры с правильными медиа файлами"""
    print("🔄 Перезапускаем контейнеры с правильными медиа файлами...")
    
    commands = [
        # Останавливаем контейнеры
        "ssh root@77.246.247.137 cd /root/tsznewproject && docker-compose down",
        
        # Удаляем старые volumes
        "ssh root@77.246.247.137 docker volume rm tsznewproject_media_files tsznewproject_static_files",
        
        # Копируем медиа файлы в правильные места
        "ssh root@77.246.247.137 cp -r /root/tsznewproject/server_media_backup/portfolio /root/tsznewproject/media/",
        "ssh root@77.246.247.137 cp -r /root/tsznewproject/server_media_backup/profile_photos /root/tsznewproject/media/",
        
        # Устанавливаем права
        "ssh root@77.246.247.137 chmod -R 755 /root/tsznewproject/media",
        
        # Запускаем контейнеры
        "ssh root@77.246.247.137 cd /root/tsznewproject && docker-compose up -d",
        
        # Ждем запуска
        "ssh root@77.246.247.137 sleep 30",
        
        # Проверяем статус
        "ssh root@77.246.247.137 cd /root/tsznewproject && docker-compose ps"
    ]
    
    for cmd in commands:
        print(f"\n📋 Выполняем: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Успешно")
                if result.stdout:
                    print(result.stdout)
            else:
                print(f"❌ Ошибка: {result.stderr}")
        except Exception as e:
            print(f"❌ Ошибка выполнения: {e}")

if __name__ == '__main__':
    restart_with_media()
