# Деплой с HTTPS поддержкой

## Что было исправлено

### 1. Nginx конфигурация (`nginx.conf`)
- Добавлен редирект с HTTP на HTTPS
- Настроен SSL сервер на порту 443
- Добавлены SSL сертификаты Let's Encrypt
- Настроены безопасные заголовки

### 2. Docker Compose (`docker-compose.yml`)
- Добавлен порт 443 для HTTPS
- Подключены SSL сертификаты к nginx контейнеру
- Обновлены ALLOWED_HOSTS для домена

### 3. Django настройки (`tsz2/settings.py`)
- Добавлены HTTPS настройки безопасности
- Настроен SECURE_SSL_REDIRECT
- Добавлены CSRF_TRUSTED_ORIGINS для HTTPS

### 4. Скрипт деплоя (`deploy_https.sh`)
- Автоматическая проверка SSL сертификата
- Получение сертификата при необходимости
- Запуск контейнеров с проверкой

## Инструкция по деплою

### 1. Подготовка
```bash
# Убедитесь, что все файлы закоммичены
git add .
git commit -m "Add HTTPS support"
git push origin main
```

### 2. Деплой на сервер
```bash
# Подключитесь к серверу
ssh root@77.246.247.137

# Перейдите в директорию проекта
cd /root/tsznewproject

# Остановите текущие контейнеры
docker-compose down

# Скопируйте новые файлы (если нужно)
git pull origin main

# Запустите деплой
chmod +x deploy_https.sh
./deploy_https.sh
```

### 3. Проверка
```bash
# Проверьте статус контейнеров
docker-compose ps

# Проверьте доступность
curl -I https://toisozvezdoi.kz
curl -I http://toisozvezdoi.kz  # должен редиректить на HTTPS
```

## Структура файлов

```
├── nginx.conf              # Конфигурация nginx с HTTPS
├── docker-compose.yml      # Docker Compose с портом 443
├── tsz2/settings.py        # Django настройки для HTTPS
├── deploy_https.sh         # Скрипт автоматического деплоя
└── DEPLOYMENT_HTTPS.md     # Эта документация
```

## Безопасность

- SSL сертификат от Let's Encrypt (бесплатный)
- Автоматическое обновление сертификата
- Безопасные заголовки HTTP
- Принудительный редирект на HTTPS
- Защита от CSRF атак

## Мониторинг

```bash
# Проверка логов
docker-compose logs nginx
docker-compose logs web

# Проверка SSL сертификата
certbot certificates

# Обновление сертификата
certbot renew
```
