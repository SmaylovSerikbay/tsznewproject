# Исправления проблемы с отображением фото профиля

## Проблема

При открытии модального окна редактирования профиля текущее фото пользователя не отображалось - показывалась только иконка пользователя.

## Причина проблемы

1. **Отсутствие инициализации фото** - функция `openEditProfileModal()` только открывала модальное окно, но не инициализировала фото
2. **Пустой src в модальном окне** - элемент `<img>` имел пустой `src=""` и был скрыт классом `hidden`
3. **Отсутствующие функции** - функции `previewProfilePhoto()` и `closeEditProfileModal()` вызывались, но не были определены

## Исправления

### 1. Обновлена функция открытия модального окна
**Файл:** `templates/dashboard-performer.html`

**Изменения:**
- Добавлена инициализация фото профиля при открытии модального окна
- Логика поиска текущего фото пользователя в интерфейсе
- Переключение между фото и иконкой

```javascript
function openEditProfileModal() {
  openModal('editProfileModal');
  
  // Инициализируем фото профиля в модальном окне
  const profilePhotoPreview = document.getElementById('profilePhotoPreview');
  const profilePhotoIcon = document.getElementById('profilePhotoIcon');
  
  if (profilePhotoPreview && profilePhotoIcon) {
    // Получаем текущее фото пользователя из основного интерфейса
    const currentProfilePhoto = document.querySelector('.profile-photo img, .user-avatar img');
    
    if (currentProfilePhoto && currentProfilePhoto.src) {
      // Если есть фото, показываем его
      profilePhotoPreview.src = currentProfilePhoto.src;
      profilePhotoPreview.classList.remove('hidden');
      profilePhotoIcon.classList.add('hidden');
    } else {
      // Если нет фото, показываем иконку
      profilePhotoPreview.classList.add('hidden');
      profilePhotoIcon.classList.remove('hidden');
    }
  }
}
```

### 2. Добавлена функция предварительного просмотра
**Файл:** `templates/dashboard-performer.html`

**Изменения:**
- Создана функция `previewProfilePhoto()` для предварительного просмотра нового фото
- Использование FileReader для чтения выбранного файла
- Обновление отображения в реальном времени

```javascript
function previewProfilePhoto(event) {
  const file = event.target.files[0];
  const profilePhotoPreview = document.getElementById('profilePhotoPreview');
  const profilePhotoIcon = document.getElementById('profilePhotoIcon');
  
  if (file && profilePhotoPreview && profilePhotoIcon) {
    const reader = new FileReader();
    reader.onload = function(e) {
      profilePhotoPreview.src = e.target.result;
      profilePhotoPreview.classList.remove('hidden');
      profilePhotoIcon.classList.add('hidden');
    };
    reader.readAsDataURL(file);
  }
}
```

### 3. Добавлена функция закрытия модального окна
**Файл:** `templates/dashboard-performer.html`

**Изменения:**
- Создана функция `closeEditProfileModal()` для закрытия модального окна
- Использование общей функции `closeModal()`

```javascript
function closeEditProfileModal() {
  closeModal('editProfileModal');
}
```

### 4. Обновлено модальное окно
**Файл:** `templates/modals/edit_profile_modal.html`

**Изменения:**
- Добавлена Django-шаблонная логика для отображения текущего фото
- Условное отображение фото или иконки при загрузке страницы
- Правильная инициализация элементов

```html
{% if user.profile_photo %}
  <img id="profilePhotoPreview" src="{{ user.profile_photo.url }}" alt="Фото профиля" class="w-full h-full object-cover">
  <i class="ri-user-line text-gray-400 text-2xl" id="profilePhotoIcon" style="display: none;"></i>
{% else %}
  <img id="profilePhotoPreview" src="" alt="Фото профиля" class="w-full h-full object-cover hidden">
  <i class="ri-user-line text-gray-400 text-2xl" id="profilePhotoIcon"></i>
{% endif %}
```

## Логика работы

### Сценарии отображения:

1. **При открытии модального окна:**
   - Если у пользователя есть фото → отображается фото
   - Если у пользователя нет фото → отображается иконка

2. **При выборе нового фото:**
   - Показывается предварительный просмотр
   - Иконка скрывается, фото показывается

3. **При сохранении:**
   - Фото сохраняется в базе данных
   - Обновляется отображение в основном интерфейсе

## Тестирование

Создан тестовый скрипт `test_profile_photo.py` для проверки:
- Наличия фото у пользователей
- URL-адресов фото
- Доступности файлов

### Запуск тестов:
```bash
python test_profile_photo.py
```

## Результат

После исправлений:
- ✅ Текущее фото отображается при открытии модального окна
- ✅ Предварительный просмотр работает при выборе нового фото
- ✅ Корректное переключение между фото и иконкой
- ✅ Все функции JavaScript определены и работают
- ✅ Улучшена пользовательская логика

## Проверка работы

### Шаги для проверки:
1. Откройте dashboard исполнителя
2. Нажмите "Редактировать профиль"
3. Убедитесь, что текущее фото отображается в модальном окне
4. Выберите новое фото и убедитесь в предварительном просмотре
5. Сохраните изменения
6. Проверьте, что фото обновилось в основном интерфейсе
