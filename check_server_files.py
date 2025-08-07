#!/usr/bin/env python3
"""
Скрипт для проверки файлов на сервере
"""

import subprocess
import os

def check_server_files():
    """Проверяет файлы на сервере"""
    print("🔍 Проверяем файлы на сервере...")
    
    # Проверяем структуру папок
    commands = [
        "ssh root@77.246.247.137 'find /root/tsznewproject/media -type f | head -20'",
        "ssh root@77.246.247.137 'ls -la /root/tsznewproject/media/'",
        "ssh root@77.246.247.137 'ls -la /root/tsznewproject/media/portfolio/ | head -10'",
        "ssh root@77.246.247.137 'ls -la /root/tsznewproject/media/profile_photos/ | head -10'"
    ]
    
    for cmd in commands:
        print(f"\n📋 Выполняем: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"❌ Ошибка: {result.stderr}")
        except Exception as e:
            print(f"❌ Ошибка выполнения: {e}")

if __name__ == '__main__':
    check_server_files()
