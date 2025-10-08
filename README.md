# TravelLux - Туристическое агентство

🌍 Современный веб-сайт туристического агентства, созданный на Django.

## ✨ Особенности

- 🏠 **Красивая главная страница** с рекомендуемыми турами
- 🗂️ **Каталог туров** с фильтрацией и поиском  
- 👤 **Система профилей** с загрузкой аватаров
- 🛒 **Корзина и бронирование** туров
- 📱 **Адаптивный дизайн** для всех устройств
- ✨ **CSS анимации** и современный UI
- 🚫 **Кастомные страницы ошибок** (404, 500, 403)

## 🚀 Развертывание на сервере

### Требования
- Python 3.9+
- Nginx
- Systemd

### Быстрая установка

```bash
# 1. Клонируем проект
git clone <repository-url>
cd Alina2

# 2. Создаем виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# 3. Устанавливаем зависимости
pip install -r requirements.txt

# 4. Настраиваем переменные окружения
cp .env.example .env
# Отредактируйте .env файл

# 5. Выполняем миграции
python manage.py migrate

# 6. Собираем статические файлы
python manage.py collectstatic

# 7. Загружаем тестовые данные
python manage.py load_sample_data

# 8. Создаем суперпользователя
python manage.py createsuperuser

# 9. Запускаем развертывание
chmod +x deploy.sh
./deploy.sh
```

### Настройка Nginx

```bash
# Копируем конфигурацию
sudo cp nginx_travellux.conf /etc/nginx/sites-available/travellux

# Создаем символическую ссылку
sudo ln -s /etc/nginx/sites-available/travellux /etc/nginx/sites-enabled/

# Проверяем конфигурацию
sudo nginx -t

# Перезапускаем Nginx
sudo systemctl restart nginx
```

### Настройка Systemd сервиса

```bash
# Копируем сервис
sudo cp travellux.service /etc/systemd/system/

# Обновляем пути в файле сервиса
sudo nano /etc/systemd/system/travellux.service

# Перезагружаем systemd
sudo systemctl daemon-reload

# Включаем автозапуск
sudo systemctl enable travellux

# Запускаем сервис
sudo systemctl start travellux

# Проверяем статус
sudo systemctl status travellux
```

### SSL сертификат (Let's Encrypt)

```bash
# Устанавливаем Certbot
sudo apt install certbot python3-certbot-nginx

# Получаем сертификат
sudo certbot --nginx -d travellux.talipovpro.uz -d www.travellux.talipovpro.uz

# Автообновление сертификата
sudo systemctl enable certbot.timer
```

## 🔧 Локальная разработка

```bash
# Клонируем проект
git clone <repository-url>
cd Alina2

# Создаем виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Настраиваем для разработки
export DEBUG=True

# Выполняем миграции
python manage.py migrate

# Загружаем тестовые данные
python manage.py load_sample_data

# Запускаем сервер разработки
python manage.py runserver
```

## 📁 Структура проекта

```
Alina2/
├── travel/                 # Основное приложение
│   ├── templates/         # HTML шаблоны
│   ├── static/           # CSS, JS, изображения
│   ├── management/       # Django команды
│   ├── models.py         # Модели данных
│   ├── views.py          # Представления
│   └── urls.py           # URL маршруты
├── travelux/             # Настройки проекта
│   ├── settings.py       # Конфигурация Django
│   ├── urls.py           # Главные URL
│   └── wsgi.py           # WSGI точка входа
├── media/                # Загруженные файлы
├── staticfiles/          # Собранные статические файлы
├── requirements.txt      # Python зависимости
├── deploy.sh            # Скрипт развертывания
└── README.md            # Документация
```

## 🎯 Основные URL

- `/` - Главная страница
- `/catalog/` - Каталог туров
- `/about/` - О компании
- `/auth/` - Авторизация
- `/profile/` - Личный кабинет
- `/admin/` - Админ панель
- `/test-errors/` - Тестирование страниц ошибок

## 📊 Управление данными

### Команды Django

```bash
# Загрузка тестовых данных
python manage.py load_sample_data

# Дополнительные данные
python manage.py add_more_data

# Создание суперпользователя
python manage.py createsuperuser

# Миграции
python manage.py makemigrations
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic
```

## 🔐 Безопасность

- ✅ CSRF защита включена
- ✅ Кастомные страницы ошибок
- ✅ Безопасные настройки для production
- ✅ Валидация форм
- ✅ Аутентификация пользователей

## 📱 Тестирование

### Локальное тестирование

```bash
# Запуск сервера разработки
python manage.py runserver

# Тестирование страниц ошибок
http://localhost:8000/test-errors/
```

### Production тестирование

```bash
# Проверка статуса сервисов
sudo systemctl status travellux
sudo systemctl status nginx

# Просмотр логов
sudo journalctl -u travellux -f
sudo tail -f /var/log/nginx/travellux_error.log
```

## 🎨 Особенности дизайна

- 🌈 **Градиентные фоны** и современные цвета
- ✨ **CSS анимации** и переходы
- 📱 **Responsive дизайн** для всех устройств
- 🎭 **Кастомные страницы ошибок** с анимацией
- 🔗 **Интуитивная навигация**

## 👥 Команда

- **Backend:** Django 5.2.7
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite (можно PostgreSQL)
- **Server:** Nginx + Gunicorn
- **Deployment:** Systemd + Let's Encrypt

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `sudo journalctl -u travellux -f`
2. Проверьте статус: `sudo systemctl status travellux`
3. Перезапустите сервис: `sudo systemctl restart travellux`

---

**TravelLux** © 2025 - Создаем незабываемые путешествия! 🌍✈️# travellux
