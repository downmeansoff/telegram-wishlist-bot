#!/bin/bash

echo "========================================"
echo "🚀 Запуск Wish List Bot"
echo "========================================"
echo ""

echo "[1/6] Проверка Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    exit 1
fi
echo "✅ Docker готов"

echo ""
echo "[2/6] Остановка старых контейнеров..."
docker-compose down -v > /dev/null 2>&1
echo "✅ Готово"

echo ""
echo "[3/6] Запуск контейнеров..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "❌ Ошибка при запуске контейнеров"
    exit 1
fi
echo "✅ Контейнеры запущены"

echo ""
echo "[4/6] Ожидание готовности PostgreSQL..."
sleep 10
echo "✅ PostgreSQL готов"

echo ""
echo "[5/6] Применение миграций..."
docker-compose exec -T backend alembic upgrade head
if [ $? -ne 0 ]; then
    echo "⚠️ Повторная попытка..."
    sleep 5
    docker-compose exec -T backend alembic upgrade head
fi
echo "✅ База данных настроена"

echo ""
echo "[6/6] Добавление категорий..."
docker-compose exec -T backend python -c "
from app.core.database import SessionLocal
from app.models.category import Category

db = SessionLocal()
categories = [
    Category(name='Электроника', emoji='💻', color='#3B82F6'),
    Category(name='Книги', emoji='📚', color='#8B5CF6'),
    Category(name='Одежда', emoji='👕', color='#EC4899'),
    Category(name='Спорт', emoji='⚽', color='#10B981'),
    Category(name='Дом', emoji='🏠', color='#F59E0B'),
    Category(name='Путешествия', emoji='✈️', color='#06B6D4'),
]
for cat in categories:
    db.add(cat)
db.commit()
print('✅ Категории добавлены!')
"

echo ""
echo "========================================"
echo "✅ Приложение успешно запущено!"
echo "========================================"
echo ""
echo "📍 Доступные URL:"
echo "   • Telegram Bot: https://t.me/iiiwishlistbot"
echo "   • Web App: http://localhost:3000"
echo "   • API: http://localhost:8000"
echo "   • API Docs: http://localhost:8000/docs"
echo ""
echo "📊 Статус контейнеров:"
docker-compose ps
echo ""
echo "📝 Просмотр логов: docker-compose logs -f"
echo "🛑 Остановка: docker-compose down"
echo ""
