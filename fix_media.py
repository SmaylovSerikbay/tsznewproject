#!/usr/bin/env python3
"""
Простой скрипт для исправления медиа файлов на сервере
"""

import subprocess

def fix_media():
    """Исправляет медиа файлы на сервере"""
    print("🔧 Исправляем медиа файлы на сервере...")
    
    # Простые команды без сложных кавычек
    commands = [
        "ssh root@77.246.247.137 ls -la /root/tsznewproject/",
        "ssh root@77.246.247.137 ls -la /root/tsznewproject/media/",
        "ssh root@77.246.247.137 mkdir -p /root/tsznewproject/media/profile_photos",
        "ssh root@77.246.247.137 ls -la /root/tsznewproject/media/portfolio/",
        "ssh root@77.246.247.137 cd /root/tsznewproject && docker-compose restart"
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
    fix_media()
