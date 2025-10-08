#!/bin/bash

# Скрипт развертывания TravelLux на сервере
echo "🚀 Начинаем развертывание TravelLux..."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Проверяем, что мы на сервере
print_status "Проверяем окружение..."

# Обновляем код из репозитория (если используется Git)
# git pull origin main

# Устанавливаем зависимости
print_status "Устанавливаем зависимости..."
pip install -r requirements.txt
pip install gunicorn

# Собираем статические файлы
print_status "Собираем статические файлы..."
python manage.py collectstatic --noinput

# Выполняем миграции
print_status "Выполняем миграции базы данных..."
python manage.py migrate

# Загружаем тестовые данные (если нужно)
print_status "Загружаем тестовые данные..."
python manage.py load_sample_data

# Создаем суперпользователя (если нужно)
print_warning "Не забудьте создать суперпользователя:"
echo "python manage.py createsuperuser"

# Устанавливаем права доступа
print_status "Настраиваем права доступа..."
chmod +x gunicorn_start.sh

print_status "Создаем необходимые директории..."
mkdir -p run
mkdir -p logs
mkdir -p staticfiles

# Перезапускаем сервисы
print_status "Перезапускаем сервисы..."
# sudo systemctl restart travellux
# sudo systemctl restart nginx

print_status "Развертывание завершено! 🎉"
print_warning "Не забудьте:"
echo "1. Скопировать nginx_travellux.conf в /etc/nginx/sites-available/"
echo "2. Создать символическую ссылку в /etc/nginx/sites-enabled/"
echo "3. Скопировать travellux.service в /etc/systemd/system/"
echo "4. Обновить пути в конфигурационных файлах"
echo "5. Настроить SSL сертификат с Let's Encrypt"

echo ""
print_status "Команды для настройки на сервере:"
echo "sudo cp nginx_travellux.conf /etc/nginx/sites-available/travellux"
echo "sudo ln -s /etc/nginx/sites-available/travellux /etc/nginx/sites-enabled/"
echo "sudo cp travellux.service /etc/systemd/system/"
echo "sudo systemctl daemon-reload"
echo "sudo systemctl enable travellux"
echo "sudo systemctl start travellux"
echo "sudo systemctl restart nginx"
echo ""
print_status "Для SSL сертификата:"
echo "sudo apt install certbot python3-certbot-nginx"
echo "sudo certbot --nginx -d travellux.talipovpro.uz -d www.travellux.talipovpro.uz"