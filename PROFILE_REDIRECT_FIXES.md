# Исправления проблемы с перенаправлением после сохранения профиля

## Проблема

После сохранения настроек профиля пользователь оставался на странице настроек профиля вместо возврата на предыдущую страницу или dashboard.

## Причина проблемы

В `profile_settings` view после успешного сохранения происходило перенаправление обратно на ту же страницу:

```python
return redirect('main:profile_settings')
```

Это создавало неудобство для пользователя, так как он ожидал возврата на предыдущую страницу.

## Решение

Реализована система умного перенаправления с использованием параметра `return_url`.

### 1. Обновлена логика в View
**Файл:** `main/views.py`

**Изменения:**
- Добавлена проверка параметра `return_url` из формы
- Реализована логика перенаправления на основе этого параметра
- Добавлено fallback перенаправление на dashboard

```python
# Определяем, куда перенаправить пользователя после сохранения
return_url = request.POST.get('return_url')
if return_url and return_url.startswith('/'):
    return redirect(return_url)
else:
    # По умолчанию возвращаемся на dashboard
    return redirect('main:dashboard')
```

### 2. Добавлены скрытые поля в формы
**Файлы:** 
- `templates/profile_settings.html`
- `templates/modals/edit_profile_modal.html`

**Изменения:**
- Добавлены скрытые поля `return_url` в обе формы
- Использование `HTTP_REFERER` для автоматического определения предыдущей страницы

```html
<!-- В основной форме -->
<input type="hidden" name="return_url" value="{{ request.GET.return_url|default:request.META.HTTP_REFERER|default:'' }}">

<!-- В модальном окне -->
<input type="hidden" name="return_url" value="{{ request.META.HTTP_REFERER|default:'' }}">
```

### 3. Обновлены ссылки на настройки профиля
**Файлы:**
- `templates/components/header.html`
- `templates/components/mobile-menu.html`
- `templates/dashboard-customer.html`
- `templates/profile.html`

**Изменения:**
- Все ссылки на настройки профиля теперь передают параметр `return_url`
- Использование `{{ request.path }}` для передачи текущего пути

```html
<!-- Было -->
<a href="{% url 'main:profile_settings' %}">

<!-- Стало -->
<a href="{% url 'main:profile_settings' %}?return_url={{ request.path }}">
```

## Логика работы

### Сценарии перенаправления:

1. **Из dashboard** → Настройки → Сохранение → Возврат на dashboard
2. **Из профиля** → Настройки → Сохранение → Возврат на профиль
3. **Из каталога** → Настройки → Сохранение → Возврат на каталог
4. **Прямой переход** → Настройки → Сохранение → Возврат на dashboard (по умолчанию)

### Приоритет перенаправления:

1. **Параметр return_url** из формы (если указан и валиден)
2. **HTTP_REFERER** (если доступен)
3. **Dashboard** (по умолчанию)

## Безопасность

- Проверка, что `return_url` начинается с `/` (внутренние ссылки)
- Fallback на dashboard при невалидном URL
- Использование Django redirect для безопасного перенаправления

## Тестирование

Создан тестовый скрипт `test_profile_redirect.py` для проверки:
- Наличия пользователей и их настроек
- Доступных городов и типов услуг
- Логики перенаправления

### Запуск тестов:
```bash
python test_profile_redirect.py
```

## Результат

После исправлений:
- ✅ Пользователь возвращается на предыдущую страницу после сохранения
- ✅ Улучшена пользовательская логика навигации
- ✅ Сохранена безопасность перенаправлений
- ✅ Добавлен fallback на dashboard
- ✅ Единообразная работа для всех форм редактирования

## Примеры использования

### Из dashboard:
```
/dashboard/ → /profile/settings/?return_url=/dashboard/ → Сохранение → /dashboard/
```

### Из профиля:
```
/profile/123/ → /profile/settings/?return_url=/profile/123/ → Сохранение → /profile/123/
```

### Из модального окна:
```
/dashboard/ → Модальное окно → Сохранение → /dashboard/
```
