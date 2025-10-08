#!/bin/bash

# Скрипт для обновления сайта на сервере
echo "🚀 Обновление TravelLux на сервере..."

echo "📦 Получение последних изменений из Git..."
git pull origin main

echo "🧹 Очистка старых статических файлов..."
rm -rf staticfiles/*

echo "📁 Сборка статических файлов..."
python manage.py collectstatic --noinput --clear

echo "🔄 Перезапуск Django сервиса..."
sudo systemctl restart travellux

echo "📊 Проверка статуса сервиса..."
sudo systemctl status travellux --no-pager -l

echo "✅ Обновление завершено!"
echo "🌐 Сайт доступен по адресу: https://travellux.talipovpro.uz"