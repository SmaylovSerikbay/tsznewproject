import os
import sys
import django

# Django-инициализация
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import User

# Сопоставление старых и новых значений service_type
SERVICE_TYPE_MAP = {
    'photographer': 'photo',
    'videographer': 'video',
    'musician': 'music',
    'host': 'host',
    'dancer': 'dance',
}

def run():
    users = User.objects.all()
    updated = 0
    for user in users:
        old_type = getattr(user, 'service_type', None)
        if old_type in SERVICE_TYPE_MAP:
            user.service_type = SERVICE_TYPE_MAP[old_type]
            user.save()
            updated += 1
    print(f'Обновлено пользователей: {updated}')

if __name__ == "__main__":
    run() 