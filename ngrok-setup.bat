@echo off
chcp 65001 >nul
echo ========================================
echo 🌐 Настройка ngrok для Web App
echo ========================================
echo.
echo Ngrok создаст HTTPS туннель к localhost:3000
echo.
echo 📋 Инструкция:
echo.
echo 1. Скачайте ngrok: https://ngrok.com/download
echo 2. Распакуйте ngrok.exe в любую папку
echo 3. Откройте новое окно командной строки
echo 4. Запустите: ngrok http 3000
echo.
echo 5. Скопируйте HTTPS URL (например: https://abc123.ngrok.io)
echo 6. Обновите .env файл:
echo    WEB_APP_URL=https://abc123.ngrok.io
echo.
echo 7. Перезапустите бота:
echo    docker-compose restart bot
echo.
echo 8. Теперь в боте появится кнопка Web App!
echo.
echo ========================================
echo.
pause
