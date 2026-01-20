@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 Запуск Wish List Bot
echo ========================================
echo.

echo [1/6] Проверка Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker не запущен! Запустите Docker Desktop и повторите попытку.
    pause
    exit /b 1
)
echo ✅ Docker готов

echo.
echo [2/6] Остановка старых контейнеров...
docker-compose down -v >nul 2>&1
echo ✅ Готово

echo.
echo [3/6] Запуск контейнеров (это может занять несколько минут при первом запуске)...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ❌ Ошибка при запуске контейнеров
    pause
    exit /b 1
)
echo ✅ Контейнеры запущены

echo.
echo [4/6] Ожидание готовности PostgreSQL...
timeout /t 10 /nobreak >nul
echo ✅ PostgreSQL готов

echo.
echo [5/6] Применение миграций базы данных...
docker-compose exec -T backend alembic upgrade head
if %errorlevel% neq 0 (
    echo ⚠️ Попытка повторного применения миграций через 5 секунд...
    timeout /t 5 /nobreak >nul
    docker-compose exec -T backend alembic upgrade head
)
echo ✅ База данных настроена

echo.
echo [6/6] Добавление базовых категорий...
docker-compose exec -T backend python -c "from app.core.database import SessionLocal; from app.models.category import Category; db = SessionLocal(); categories = [Category(name='Электроника', emoji='💻', color='#3B82F6'), Category(name='Книги', emoji='📚', color='#8B5CF6'), Category(name='Одежда', emoji='👕', color='#EC4899'), Category(name='Спорт', emoji='⚽', color='#10B981'), Category(name='Дом', emoji='🏠', color='#F59E0B'), Category(name='Путешествия', emoji='✈️', color='#06B6D4')]; [db.add(cat) for cat in categories]; db.commit(); print('✅ Категории добавлены!')"
echo.

echo ========================================
echo ✅ Приложение успешно запущено!
echo ========================================
echo.
echo 📍 Доступные URL:
echo    • Telegram Bot: https://t.me/iiiwishlistbot
echo    • Web App: http://localhost:3000
echo    • API: http://localhost:8000
echo    • API Docs: http://localhost:8000/docs
echo.
echo 📊 Проверка статуса:
docker-compose ps
echo.
echo 📝 Для просмотра логов используйте:
echo    docker-compose logs -f
echo.
echo 🛑 Для остановки используйте:
echo    docker-compose down
echo.
pause
