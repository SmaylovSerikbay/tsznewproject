#!/usr/bin/env python3
"""
Скрипт для исправления медиа файлов в Docker
"""

import subprocess

def fix_docker_media():
    """Исправляет медиа файлы в Docker"""
    print("🔧 Исправляем медиа файлы в Docker...")
    
    commands = [
        # Создаем папки в контейнере
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 mkdir -p /app/media/portfolio",
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 mkdir -p /app/media/profile_photos",
        
        # Копируем файлы из backup в правильные папки
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 cp -r /app/server_media_backup/portfolio/* /app/media/portfolio/",
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 cp -r /app/server_media_backup/profile_photos/* /app/media/profile_photos/",
        
        # Устанавливаем правильные права
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 chown -R app:app /app/media",
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 chmod -R 755 /app/media",
        
        # Проверяем результат
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 ls -la /app/media/",
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 ls -la /app/media/portfolio/ | head -5",
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 ls -la /app/media/profile_photos/ | head -5"
    ]
    
    for cmd in commands:
        print(f"\n📋 Выполняем: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Успешно")
                print(result.stdout)
            else:
                print(f"❌ Ошибка: {result.stderr}")
        except Exception as e:
            print(f"❌ Ошибка выполнения: {e}")

if __name__ == '__main__':
    fix_docker_media()
