# TSZ30 - Платформа для поиска исполнителей

Веб-приложение для поиска и бронирования услуг исполнителей (фотографы, музыканты, ведущие и др.).

## 🚀 Быстрый старт с Docker

### Предварительные требования

- Docker
- Docker Compose
- Git

### Установка и запуск

1. **Клонируйте репозиторий:**
```bash
git clone <your-repo-url>
cd tsz30
```

2. **Запустите приложение:**
```bash
docker-compose up -d
```

3. **Откройте браузер:**
```
http://localhost
```

## 📋 Миграция с SQLite на PostgreSQL

Если у вас есть существующие данные в SQLite, выполните следующие шаги:

### 1. Экспорт данных из SQLite
```bash
python migrate_to_postgres.py
```

### 2. Запуск с PostgreSQL
```bash
docker-compose up -d
```

### 3. Импорт данных в PostgreSQL
```bash
docker-compose exec web python import_to_postgres.py
```

## 🔧 Разработка

### Локальная разработка

1. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Настройте базу данных:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. **Запустите сервер разработки:**
```bash
python manage.py runserver
```

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🐳 Docker конфигурация

### Сервисы

- **web** - Django приложение (порт 8000)
- **db** - PostgreSQL база данных (порт 5432)
- **nginx** - Веб-сервер (порт 80)

### Команды Docker

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка сервисов
docker-compose down

# Пересборка образов
docker-compose build --no-cache

# Выполнение команд в контейнере
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## 📁 Структура проекта

```
tsz30/
├── main/                    # Основное Django приложение
│   ├── models.py           # Модели данных
│   ├── views.py            # Представления
│   ├── urls.py             # URL маршруты
│   └── migrations/         # Миграции базы данных
├── templates/              # HTML шаблоны
├── static/                 # Статические файлы
├── media/                  # Загруженные файлы
├── tsz2/                   # Настройки Django
│   ├── settings.py         # Основные настройки
│   └── urls.py             # Главные URL маршруты
├── docker-compose.yml      # Docker Compose конфигурация
├── Dockerfile              # Docker образ
├── nginx.conf              # Nginx конфигурация
├── requirements.txt        # Python зависимости
└── README.md              # Документация
```

## 🔒 Безопасность

### Продакшен настройки

1. **Измените SECRET_KEY:**
```env
SECRET_KEY=your-very-secure-secret-key
```

2. **Отключите DEBUG:**
```env
DEBUG=False
```

3. **Настройте ALLOWED_HOSTS:**
```env
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

4. **Используйте HTTPS:**
```bash
# Добавьте SSL сертификаты в nginx.conf
```

## 📊 Мониторинг

### Логи

```bash
# Логи Django
docker-compose logs web

# Логи Nginx
docker-compose logs nginx

# Логи PostgreSQL
docker-compose logs db
```

### Резервное копирование

```bash
# Резервная копия базы данных
docker-compose exec db pg_dump -U tsz30_user tsz30_db > backup.sql

# Восстановление базы данных
docker-compose exec -T db psql -U tsz30_user tsz30_db < backup.sql
```

## 🚀 Деплой на сервер

### 1. Подготовка сервера

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Клонирование и запуск

```bash
git clone <your-repo-url>
cd tsz30

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env файл

# Запуск
docker-compose up -d
```

### 3. Настройка домена

1. Настройте DNS записи
2. Обновите ALLOWED_HOSTS в .env
3. Настройте SSL сертификаты

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📝 Лицензия

Этот проект лицензирован под MIT License.

## 📞 Поддержка

Если у вас есть вопросы или проблемы, создайте Issue в репозитории.
