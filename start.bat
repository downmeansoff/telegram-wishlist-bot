@echo off
chcp 65001 >nul
cls
echo ========================================
echo 🚀 Wish List Bot - Быстрый запуск
echo ========================================
echo.

echo [1/3] Запуск Docker контейнеров...
docker-compose up -d

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка! Убедитесь, что Docker Desktop запущен.
    echo.
    pause
    exit /b 1
)

echo ✅ Контейнеры запущены
echo.

echo [2/3] Проверка состояния сервисов...
timeout /t 3 /nobreak >nul
docker-compose ps

echo.
echo [3/3] Проверка API...
timeout /t 2 /nobreak >nul
curl -s http://localhost:8000/health

echo.
echo.
echo ========================================
echo ✅ Приложение запущено!
echo ========================================
echo.
echo 📍 Доступные URL:
echo    • Telegram Bot: https://t.me/iiiwishlistbot
echo    • Web App: http://localhost:3000
echo    • API Docs: http://localhost:8000/docs
echo.
echo 📝 Логи: docker-compose logs -f
echo 🛑 Остановка: docker-compose down
echo.
pause
