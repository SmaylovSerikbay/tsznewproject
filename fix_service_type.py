from main.models import User

# Соответствие старых и новых значений
mapping = {
    'photographer': 'photo',
    'videographer': 'video',
    'musician': 'music',
    'host': 'host',
    'dance': 'dance',
    'decorator': 'host',  # если был декоратор, делаем ведущим (или поменяйте на нужное)
    'makeup': 'dance',    # если был визажист, делаем шоу-программой (или поменяйте на нужное)
}

changed = 0
for user in User.objects.filter(user_type='performer'):
    st = user.service_type
    if st in mapping:
        user.service_type = mapping[st]
        user.save()
        changed += 1
        print(f"User {user.id} ({user.get_full_name()}): {st} -> {user.service_type}")
    else:
        print(f"User {user.id} ({user.get_full_name()}): {st}")
print(f"\nИсправлено исполнителей: {changed}") 