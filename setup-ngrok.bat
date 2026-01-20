@echo off
chcp 65001 >nul
cls
echo ========================================
echo 🌐 Настройка HTTPS для Web App
echo ========================================
echo.
echo Открываю страницу загрузки ngrok...
start https://ngrok.com/download
echo.
echo ========================================
echo 📋 ИНСТРУКЦИЯ:
echo ========================================
echo.
echo 1. На открывшейся странице:
echo    - Нажмите "Download for Windows"
echo    - Сохраните файл ngrok.zip
echo.
echo 2. Распакуйте ngrok.zip в эту папку:
echo    %CD%
echo.
echo 3. После распаковки нажмите любую клавишу здесь
echo.
pause
echo.
echo Проверяю наличие ngrok.exe...
if exist ngrok.exe (
    echo ✅ ngrok.exe найден!
    echo.
    echo Запускаю ngrok...
    echo.
    echo ========================================
    echo ВАЖНО: НЕ ЗАКРЫВАЙТЕ ЭТО ОКНО!
    echo ========================================
    echo.
    echo Сейчас запустится ngrok и создаст HTTPS туннель.
    echo Вы увидите строку вроде:
    echo.
    echo   Forwarding  https://abc123.ngrok-free.app -> localhost:3000
    echo.
    echo СКОПИРУЙТЕ этот HTTPS URL (начинается с https://)
    echo.
    pause
    echo.
    start cmd /k ngrok http 3000
    echo.
    echo ========================================
    echo Ngrok запущен в новом окне!
    echo ========================================
    echo.
    echo СЛЕДУЮЩИЙ ШАГ:
    echo.
    echo 1. Найдите в окне ngrok строку "Forwarding"
    echo 2. Скопируйте HTTPS URL (например: https://abc123.ngrok-free.app)
    echo 3. Вернитесь сюда и вставьте URL:
    echo.
    set /p NGROK_URL="Вставьте HTTPS URL: "

    if "%NGROK_URL%"=="" (
        echo ❌ URL не введен!
        pause
        exit /b 1
    )

    echo.
    echo Обновляю .env файл...

    REM Создаем временный файл
    set TEMP_FILE=%TEMP%\env_temp.txt

    REM Читаем .env и заменяем WEB_APP_URL
    (for /f "delims=" %%a in (.env) do (
        set "line=%%a"
        setlocal enabledelayedexpansion
        if "!line:~0,12!"=="WEB_APP_URL=" (
            echo WEB_APP_URL=%NGROK_URL%
        ) else (
            echo !line!
        )
        endlocal
    )) > "%TEMP_FILE%"

    REM Заменяем оригинальный файл
    move /y "%TEMP_FILE%" .env >nul

    echo ✅ .env обновлен!
    echo.
    echo Перезапускаю бота...
    docker-compose restart bot

    echo.
    echo ========================================
    echo ✅ ГОТОВО!
    echo ========================================
    echo.
    echo Web App теперь доступен по адресу:
    echo %NGROK_URL%
    echo.
    echo Откройте Telegram бота:
    echo https://t.me/iiiwishlistbot
    echo.
    echo Отправьте: /start
    echo.
    echo Теперь вы увидите кнопку "🎁 Мои желания"!
    echo.
    echo ========================================
    echo ВАЖНО: Не закрывайте окно ngrok!
    echo ========================================
    echo Пока ngrok работает, Web App будет доступен.
    echo Если закроете ngrok - Web App перестанет работать.
    echo.
    pause
) else (
    echo ❌ ngrok.exe не найден!
    echo.
    echo Пожалуйста:
    echo 1. Скачайте ngrok с https://ngrok.com/download
    echo 2. Распакуйте ngrok.exe в папку:
    echo    %CD%
    echo 3. Запустите этот скрипт снова
    echo.
    pause
)
