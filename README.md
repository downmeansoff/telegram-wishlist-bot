# 🎁 Telegram Wish List Bot

Полнофункциональный Telegram-бот с встроенным Web App для управления списками желаний.

## 🌟 Возможности

### Telegram Bot
- 🤖 Команды: `/start`, `/add`, `/list`, `/share`
- ⚡ Быстрое добавление желаний через текст
- 📱 Inline-кнопки для запуска Web App
- 🔔 Умные уведомления о днях рождения

### Web App
- 🎨 Красивые карточки желаний с фото
- 🔄 Drag & drop для изменения приоритета
- 👥 Групповые списки для дарителей
- 📊 Статистика и аналитика
- 🔗 Автопарсинг ссылок (Ozon, Wildberries, AliExpress)
- 🎯 Фильтры, поиск, категории

### Групповые функции
- 👫 Создание групп друзей/семьи
- 🎂 Календарь дней рождений
- 🔒 Бронирование подарков (невидимо для получателя)
- 💬 Обсуждение подарков

## 🏗️ Архитектура

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│  Telegram   │─────▶│   Bot API    │─────▶│   Backend    │
│   Client    │      │  (aiogram)   │      │  (FastAPI)   │
└─────────────┘      └──────────────┘      └──────────────┘
       │                                           │
       │                                           │
       ▼                                           ▼
┌─────────────┐                            ┌──────────────┐
│   Web App   │───────────────────────────▶│  PostgreSQL  │
│   (React)   │                            │   + Redis    │
└─────────────┘                            └──────────────┘
```

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))
- Node.js 18+ и Python 3.10+ (для разработки без Docker)

### Установка

1. **Клонируйте репозиторий**
```bash
git clone <your-repo-url>
cd website
```

2. **Создайте .env файл**
```bash
cp .env.example .env
```

3. **Настройте переменные окружения**

Откройте `.env` и заполните:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
SECRET_KEY=generate_random_32_char_string
POSTGRES_PASSWORD=your_secure_password
```

Для генерации SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

4. **Запустите проект**
```bash
docker-compose up -d
```

5. **Примените миграции базы данных**
```bash
docker-compose exec backend alembic upgrade head
```

6. **Готово! 🎉**

- 🤖 Bot: Найдите вашего бота в Telegram
- 🌐 Web App: http://localhost:3000
- 📡 API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

## 📁 Структура проекта

```
website/
├── backend/                 # Python Backend
│   ├── app/
│   │   ├── api/            # FastAPI endpoints
│   │   ├── bot/            # Telegram bot handlers
│   │   ├── core/           # Config, security, database
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/               # React Web App
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── hooks/         # Custom hooks
│   │   ├── utils/         # Utilities
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile.dev
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🛠️ Разработка

### Backend (без Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Запустите PostgreSQL и Redis локально или через Docker
docker-compose up -d postgres redis

# Миграции
alembic upgrade head

# Запустите API
uvicorn app.main:app --reload

# В отдельном терминале запустите бота
python -m app.bot.main
```

### Frontend (без Docker)

```bash
cd frontend
npm install
npm start
```

### Создание новой миграции

```bash
docker-compose exec backend alembic revision --autogenerate -m "Description"
docker-compose exec backend alembic upgrade head
```

## 🔧 Конфигурация бота

### Создание бота в BotFather

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в `.env`

### Настройка Menu Button (для Web App)

```bash
# Отправьте BotFather:
/mybots
# Выберите вашего бота
# Menu Button -> Configure Menu Button -> URL
# Введите: https://your-domain.com
```

## 🌐 Деплой в продакшн

### Backend (Railway/Render)

1. Создайте PostgreSQL базу данных
2. Добавьте переменные окружения:
   - `DATABASE_URL`
   - `TELEGRAM_BOT_TOKEN`
   - `SECRET_KEY`
   - `WEB_APP_URL`
   - `ENVIRONMENT=production`

3. Деплой:
```bash
# Railway
railway up

# Render
# Подключите GitHub репозиторий и настройте build command:
# Build: pip install -r requirements.txt
# Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel/Netlify)

```bash
# Vercel
cd frontend
vercel --prod

# Netlify
npm run build
netlify deploy --prod --dir=build
```

### Настройка Webhook (опционально)

Для продакшна рекомендуется использовать webhook вместо polling:

```python
# В .env
TELEGRAM_BOT_WEBHOOK_URL=https://your-backend-domain.com/api/webhook

# Bot автоматически настроит webhook при запуске
```

## 📊 База данных

### Схема

- **users** - Пользователи Telegram
- **wishes** - Желания пользователей
- **categories** - Категории желаний
- **groups** - Группы друзей/семьи
- **group_members** - Участники групп
- **reservations** - Бронирования подарков
- **notifications** - Уведомления

### Резервное копирование

```bash
# Backup
docker-compose exec postgres pg_dump -U wishlist_user wishlist_db > backup.sql

# Restore
docker-compose exec -T postgres psql -U wishlist_user wishlist_db < backup.sql
```

## 🧪 Тестирование

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 API Документация

После запуска проекта документация доступна:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 Безопасность

- ✅ Валидация Telegram WebApp initData
- ✅ CORS настройки
- ✅ Rate limiting
- ✅ SQL injection защита (SQLAlchemy ORM)
- ✅ XSS защита (React автоэскейпинг)
- ✅ Хеширование паролей (для будущих фич)

## 🤝 Содействие

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

## 🆘 Поддержка

- 📧 Email: support@example.com
- 💬 Telegram: @your_support_channel
- 🐛 Issues: GitHub Issues

## 🎯 Roadmap

- [ ] Интеграция с платежными системами
- [ ] Мобильные приложения (React Native)
- [ ] AI рекомендации подарков
- [ ] Интеграция с календарями (Google Calendar)
- [ ] Экспорт в PDF
- [ ] Темная тема
- [ ] Мультиязычность

---

Сделано с ❤️ для управления желаниями
