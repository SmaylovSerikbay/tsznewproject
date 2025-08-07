#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User, ServiceType

def fix_service_type_migration():
    """Исправляет существующих пользователей с неправильными значениями service_type"""
    
    # Сопоставление старых строковых значений с кодами ServiceType
    SERVICE_TYPE_MAP = {
        'photo': 'photo',
        'video': 'video', 
        'music': 'music',
        'host': 'host',
        'dance': 'dance',
        'restaurant': 'restaurant',
        'makeup': 'makeup',
        'registry': 'registry',
        'star': 'star',
        'cottage': 'cottage',
        'recreation_areas': 'recreation_areas',
        'aphishe': 'aphishe'
    }
    
    # Получаем всех пользователей-исполнителей
    performers = User.objects.filter(user_type='performer')
    
    fixed_count = 0
    for user in performers:
        try:
            # Проверяем, есть ли у пользователя service_type как строка
            if hasattr(user, 'service_type') and user.service_type:
                # Если service_type - это строка (старый формат)
                if isinstance(user.service_type, str):
                    old_type = user.service_type
                    if old_type in SERVICE_TYPE_MAP:
                        # Находим соответствующий объект ServiceType
                        try:
                            service_type_obj = ServiceType.objects.get(code=SERVICE_TYPE_MAP[old_type])
                            user.service_type = service_type_obj
                            user.save()
                            print(f"Исправлен пользователь {user.id} ({user.get_full_name()}): {old_type} -> {service_type_obj.name}")
                            fixed_count += 1
                        except ServiceType.DoesNotExist:
                            print(f"Ошибка: ServiceType с кодом {SERVICE_TYPE_MAP[old_type]} не найден для пользователя {user.id}")
                    else:
                        print(f"Неизвестный тип услуги '{old_type}' для пользователя {user.id}")
                # Если service_type уже является объектом ServiceType, пропускаем
                elif hasattr(user.service_type, 'code'):
                    print(f"Пользователь {user.id} уже имеет правильный формат service_type")
                else:
                    print(f"Неизвестный формат service_type для пользователя {user.id}: {type(user.service_type)}")
            else:
                print(f"Пользователь {user.id} не имеет service_type")
                
        except Exception as e:
            print(f"Ошибка при обработке пользователя {user.id}: {e}")
    
    print(f"\nВсего исправлено пользователей: {fixed_count}")
    print(f"Всего исполнителей в базе: {performers.count()}")

if __name__ == '__main__':
    fix_service_type_migration() 