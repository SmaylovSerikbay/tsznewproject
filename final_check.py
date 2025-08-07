#!/usr/bin/env python3
"""
Финальная проверка и перезапуск
"""

import subprocess

def final_check():
    """Финальная проверка и перезапуск"""
    print("🔍 Финальная проверка...")
    
    commands = [
        # Проверяем файлы
        "ssh root@77.246.247.137 ls -la /root/tsznewproject/media/",
        "ssh root@77.246.247.137 ls -la /root/tsznewproject/media/portfolio/ | head -3",
        "ssh root@77.246.247.137 ls -la /root/tsznewproject/media/profile_photos/ | head -3",
        
        # Перезапускаем контейнеры
        "ssh root@77.246.247.137 cd /root/tsznewproject && docker-compose restart",
        
        # Проверяем статус
        "ssh root@77.246.247.137 cd /root/tsznewproject && docker-compose ps"
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
    final_check()
