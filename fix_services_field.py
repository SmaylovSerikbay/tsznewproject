import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsz2.settings')
django.setup()

from main.models import Order

SERVICE_MAP = {
    'Фотограф': 'photo',
    'Видеограф': 'video',
    'Музыканты': 'music',
    'Ведущий': 'host',
    'Шоу-программа': 'dance',
}

orders = Order.objects.all()
for order in orders:
    services = order.services
    if not services:
        continue
    changed = False
    new_services = []
    for s in services:
        if s in SERVICE_MAP:
            new_services.append(SERVICE_MAP[s])
            changed = True
        else:
            new_services.append(s)
    if changed:
        order.services = new_services
        order.save()
        print(f'Order {order.id} updated: {new_services}')
print('Done!') 