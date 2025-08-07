import os
import sys

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(__file__))

# Устанавливаем переменную окружения для продакшен настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings_production')

# Импортируем WSGI приложение
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 