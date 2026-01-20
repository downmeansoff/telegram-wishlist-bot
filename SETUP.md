# 🚀 Инструкция по установке и настройке

## Шаг 1: Предварительные требования

Убедитесь, что у вас установлено:

- **Docker Desktop** (для Windows/Mac) или Docker Engine (для Linux)
- **Docker Compose** v2.0+
- **Git**

Проверить версии:
```bash
docker --version
docker-compose --version
git --version
```

## Шаг 2: Создание Telegram бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)

2. Отправьте команду `/newbot`

3. Следуйте инструкциям:
   - Придумайте имя бота (например: "My Wish List Bot")
   - Придумайте username (например: "my_wishlist_bot")

4. **Сохраните токен**, который выдаст BotFather. Он выглядит так:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

5. Настройте меню бота (опционально):
   ```
   /mybots → Выберите вашего бота → Bot Settings → Menu Button → Configure menu button
   ```
   - URL: `https://your-domain.com` (замените на ваш домен или оставьте пустым для локальной разработки)

## Шаг 3: Клонирование и настройка проекта

1. Склонируйте проект:
```bash
git clone <your-repo-url>
cd website
```

2. Создайте `.env` файл:
```bash
cp .env.example .env
```

3. Откройте `.env` в текстовом редакторе и заполните:

```env
# Данные PostgreSQL (можно оставить как есть для локальной разработки)
POSTGRES_DB=wishlist_db
POSTGRES_USER=wishlist_user
POSTGRES_PASSWORD=your_secure_password_here_12345

# Telegram Bot (ВАЖНО!)
TELEGRAM_BOT_TOKEN=ваш_токен_от_botfather
TELEGRAM_BOT_WEBHOOK_URL=
REACT_APP_TELEGRAM_BOT_USERNAME=ваш_username_бота

# Secret Key (сгенерируйте)
SECRET_KEY=your_secret_key_min_32_characters_long_abc123

# URLs (для локальной разработки оставьте как есть)
WEB_APP_URL=http://localhost:3000
API_URL=http://localhost:8000
REACT_APP_API_URL=http://localhost:8000

# Окружение
ENVIRONMENT=development
```

**Как сгенерировать SECRET_KEY:**

Windows PowerShell:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Linux/Mac:
```bash
openssl rand -base64 32
```

## Шаг 4: Запуск проекта

1. **Запустите Docker контейнеры:**

```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL (порт 5432)
- Redis (порт 6379)
- Backend API (порт 8000)
- Telegram Bot
- Frontend (порт 3000)

2. **Дождитесь запуска** (первый запуск может занять 2-3 минуты):

```bash
# Проверить статус
docker-compose ps

# Посмотреть логи
docker-compose logs -f
```

3. **Примените миграции базы данных:**

```bash
docker-compose exec backend alembic upgrade head
```

4. **Добавьте базовые категории** (опционально):

```bash
docker-compose exec backend python -c "
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
print('Категории добавлены!')
"
```

## Шаг 5: Проверка работы

1. **Проверьте API:**
   - Откройте http://localhost:8000/health
   - Должны увидеть: `{"status":"healthy","environment":"development","version":"1.0.0"}`

2. **Проверьте API документацию:**
   - Swagger: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Проверьте Frontend:**
   - Откройте http://localhost:3000
   - Должна загрузиться главная страница

4. **Проверьте Telegram бота:**
   - Найдите вашего бота в Telegram
   - Отправьте `/start`
   - Должно прийти приветственное сообщение с кнопками

## Шаг 6: Тестирование Web App

### Вариант 1: Через Telegram (рекомендуется)

1. В чате с ботом нажмите кнопку **"🎁 Мои желания"**
2. Откроется Web App внутри Telegram

### Вариант 2: Через браузер (для разработки)

1. Откройте Chrome DevTools (F12)
2. Перейдите в Console
3. Вставьте код для эмуляции Telegram:

```javascript
window.Telegram = {
  WebApp: {
    initData: "",
    initDataUnsafe: {
      user: {
        id: 123456789,
        first_name: "Test",
        last_name: "User",
        username: "testuser"
      }
    },
    expand: () => {},
    ready: () => {},
    enableClosingConfirmation: () => {},
    setHeaderColor: () => {},
    colorScheme: "light"
  }
}
```

4. Перезагрузите страницу

## Шаг 7: Остановка и перезапуск

```bash
# Остановить все контейнеры
docker-compose stop

# Остановить и удалить контейнеры
docker-compose down

# Остановить и удалить контейнеры + volumes (очистит БД!)
docker-compose down -v

# Перезапустить
docker-compose restart

# Пересобрать и запустить заново
docker-compose up -d --build
```

## Устранение проблем

### Ошибка: "Port already in use"

```bash
# Найти процесс на порту 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac

# Убить процесс
taskkill /PID <PID> /F         # Windows
kill -9 <PID>                  # Linux/Mac
```

### Ошибка: "Cannot connect to database"

```bash
# Проверить, запущен ли PostgreSQL
docker-compose ps

# Пересоздать базу данных
docker-compose down -v
docker-compose up -d postgres
docker-compose exec backend alembic upgrade head
```

### Бот не отвечает

1. Проверьте токен в `.env`
2. Проверьте логи:
   ```bash
   docker-compose logs bot
   ```
3. Убедитесь, что контейнер запущен:
   ```bash
   docker-compose ps
   ```

### Web App не загружается

1. Проверьте CORS настройки в [backend/app/main.py](backend/app/main.py)
2. Убедитесь, что frontend собрался:
   ```bash
   docker-compose logs frontend
   ```

## Следующие шаги

✅ Проект запущен локально!

Теперь вы можете:

1. **Добавить желания** через бота или Web App
2. **Создать группы** и пригласить друзей
3. **Настроить внешний вид** в [frontend/src/index.css](frontend/src/index.css)
4. **Добавить новые функции** в код

### Деплой в продакшн

См. [README.md](README.md) раздел "Деплой в продакшн"

## Полезные команды

```bash
# Логи всех сервисов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f backend
docker-compose logs -f bot
docker-compose logs -f frontend

# Войти в контейнер
docker-compose exec backend bash
docker-compose exec postgres psql -U wishlist_user wishlist_db

# Создать новую миграцию
docker-compose exec backend alembic revision --autogenerate -m "Description"
docker-compose exec backend alembic upgrade head

# Запустить тесты
docker-compose exec backend pytest

# Установить новые пакеты
docker-compose exec backend pip install package_name
docker-compose exec frontend npm install package-name

# Пересобрать после изменений
docker-compose up -d --build
```

## Поддержка

Если что-то не работает:
1. Проверьте логи: `docker-compose logs`
2. Проверьте `.env` файл
3. Создайте issue на GitHub
