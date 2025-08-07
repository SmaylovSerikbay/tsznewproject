# Исправления проблем с бронированием

## Исправленные проблемы

### 1. Ошибка 404 при бронировании
**Проблема**: После бронирования возникала ошибка 404 на URL `/create-order-booking/5/`

**Причины**: 
1. Неправильный URL в JavaScript (`/create-order-booking/` вместо `/create-order/`)
2. Неправильный redirect в конце функции `create_order_booking`

**Исправления**: 
1. **В `static/js/main.js`**: Изменил `action="/create-order-booking/${performerId}/"` на `action="/create-order/${performerId}/"`
2. **В `main/views.py`**: Изменил `return redirect('main:profile', performer_id)` на `return redirect('main:view_profile', user_id=performer_id)`
- Теперь после успешного бронирования пользователь перенаправляется на детали заказа

### 2. Логика принятия бронирований исполнителями
**Проблема**: Исполнители не видели прямые бронирования в своем dashboard

**Исправления**:

#### В `main/views.py` - функция `dashboard`:
1. **Добавлена логика для прямых бронирований**:
   ```python
   # 1. Прямые бронирования (order_type='booking')
   booking_orders = Order.objects.filter(
       performer=request.user,
       order_type='booking',
       status__in=['in_progress', 'new']
   )
   active_orders.extend(booking_orders)
   ```

2. **Добавлена статистика активных бронирований**:
   ```python
   active_bookings_count = Order.objects.filter(
       performer=request.user,
       order_type='booking',
       status__in=['in_progress', 'new']
   ).count()
   ```

3. **Обновлен контекст для шаблона**:
   - Добавлен `'active_bookings_count': active_bookings_count`

#### В `templates/dashboard-performer.html`:
1. **Добавлена карточка статистики для активных бронирований**:
   ```html
   <div class="stat-card">
     <i class="ri-calendar-check-line"></i>
     <div class="stat-value">{{ active_bookings_count }}</div>
     <div class="stat-label">Активных бронирований</div>
   </div>
   ```

2. **Улучшено отображение типа заказа**:
   ```html
   {% if order.order_type == 'booking' %}
     <i class="ri-calendar-check-line"></i> Прямое бронирование
   {% else %}
     <i class="ri-file-list-line"></i> Заявка-запрос
   {% endif %}
   ```

3. **Исправлена статистика новых заявок**:
   - Изменил `{{ active_orders_count }}` на `{{ new_requests_count }}`

### 3. Улучшения календаря
**Проблема**: Старый input type="date" был избыточен рядом с красивым календарем

**Исправления**:

#### В `static/js/main.js`:
1. **Заменил input type="date" на hidden input**:
   ```javascript
   <input type="hidden" id="event_date" name="event_date" required>
   ```

2. **Добавлено отображение выбранной даты на кнопке**:
   ```javascript
   function selectDate(dateString) {
       // Форматируем дату для отображения
       const formattedDate = date.toLocaleDateString('ru-RU', {
           day: '2-digit',
           month: '2-digit',
           year: 'numeric'
       });
       
       // Обновляем текст кнопки
       calendarBtn.innerHTML = `<i class="ri-calendar-line"></i> ${formattedDate}`;
       calendarBtn.classList.add('has-date');
   }
   ```

#### В `static/css/style.css`:
1. **Стилизация кнопки календаря как поля ввода**:
   ```css
   .calendar-btn {
     width: 100%;
     justify-content: flex-start;
     background: white;
     border: 2px solid var(--gray-200);
     color: var(--text-secondary);
     text-align: left;
   }
   
   .calendar-btn.has-date {
     color: var(--text-primary);
     border-color: var(--primary-color);
   }
   ```

## Результат

1. ✅ **Бронирование работает без ошибок 404**
2. ✅ **Исполнители видят прямые бронирования в dashboard**
3. ✅ **Добавлена статистика активных бронирований**
4. ✅ **Улучшен интерфейс календаря (убран дублирующий input)**
5. ✅ **Кнопка календаря показывает выбранную дату**
6. ✅ **Красные даты в календаре работают корректно**

## Тестирование

Для проверки исправлений:

1. **Войдите как заказчик** (`+77776875411`)
2. **Перейдите в каталог исполнителей**
3. **Нажмите "Забронировать" на любом исполнителе**
4. **Выберите дату в календаре** (красные даты должны быть недоступны)
5. **Заполните форму и отправьте**
6. **Должно произойти перенаправление на детали заказа без ошибки 404**

7. **Войдите как исполнитель** (`+77085446945`)
8. **Перейдите в dashboard**
9. **Проверьте секцию "Мои заказы"** - там должны появиться прямые бронирования
10. **Проверьте статистику** - должна быть карточка "Активных бронирований" 