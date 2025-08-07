#!/usr/bin/env python3
"""
Скрипт для проверки Docker volumes
"""

import subprocess

def check_docker_volumes():
    """Проверяет Docker volumes"""
    print("🔍 Проверяем Docker volumes...")
    
    commands = [
        "ssh root@77.246.247.137 docker volume ls",
        "ssh root@77.246.247.137 docker volume inspect tsznewproject_media_files",
        "ssh root@77.246.247.137 docker volume inspect tsznewproject_static_files",
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 ls -la /app/media/",
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 ls -la /app/media/portfolio/",
        "ssh root@77.246.247.137 docker exec tsznewproject-web-1 ls -la /app/media/profile_photos/"
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
    check_docker_volumes()
