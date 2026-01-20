# 🤝 Contributing Guide

Спасибо за интерес к проекту! Этот гайд поможет вам внести свой вклад.

## Начало работы

1. **Fork репозитория**
2. **Клонируйте свой fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/wishlist-bot.git
   cd wishlist-bot
   ```
3. **Создайте ветку для изменений:**
   ```bash
   git checkout -b feature/amazing-feature
   ```

## Структура проекта

```
website/
├── backend/              # Python backend
│   ├── app/
│   │   ├── api/         # FastAPI endpoints
│   │   ├── bot/         # Telegram bot
│   │   ├── core/        # Config, database
│   │   ├── models/      # SQLAlchemy models
│   │   └── schemas/     # Pydantic schemas
│   └── alembic/         # DB migrations
│
└── frontend/            # React frontend
    └── src/
        ├── components/  # React components
        ├── pages/       # Pages
        ├── services/    # API services
        └── hooks/       # Custom hooks
```

## Разработка

### Backend

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Запустить API
uvicorn app.main:app --reload

# Запустить бота
python -m app.bot.main

# Создать миграцию
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Frontend

```bash
cd frontend

# Установить зависимости
npm install

# Запустить dev server
npm run dev

# Собрать для продакшна
npm run build
```

## Стиль кода

### Python
- Следуйте PEP 8
- Используйте type hints
- Документируйте функции docstrings

```python
async def get_user(user_id: int, session: AsyncSession) -> User:
    """
    Get user by ID

    Args:
        user_id: User ID
        session: Database session

    Returns:
        User object

    Raises:
        HTTPException: If user not found
    """
    pass
```

### TypeScript/React
- Используйте функциональные компоненты
- Используйте TypeScript для типизации
- Следуйте React best practices

```typescript
interface Props {
  title: string
  onClose: () => void
}

export default function Component({ title, onClose }: Props) {
  // ...
}
```

## Коммиты

Используйте понятные сообщения коммитов:

```
feat: Add wish sharing feature
fix: Fix pagination in wish list
docs: Update setup instructions
style: Format code with black
refactor: Simplify wish creation logic
test: Add tests for user API
```

## Pull Request

1. **Обновите свою ветку:**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Протестируйте изменения:**
   ```bash
   # Backend
   pytest

   # Frontend
   npm test
   ```

3. **Создайте PR:**
   - Опишите изменения
   - Прикрепите скриншоты (для UI изменений)
   - Упомяните связанные issues

4. **Дождитесь ревью**

## Что можно улучшить

### Features
- [ ] Уведомления о днях рождения
- [ ] Парсинг цен с сайтов
- [ ] Экспорт списка в PDF
- [ ] Темная тема
- [ ] Мультиязычность
- [ ] Поиск подарков по AI

### Улучшения
- [ ] Добавить тесты
- [ ] Оптимизировать запросы к БД
- [ ] Улучшить UX
- [ ] Добавить анимации

### Документация
- [ ] API documentation
- [ ] User guide
- [ ] Video tutorials

## Вопросы?

- Создайте issue
- Напишите в discussions
- Telegram: @your_support

Спасибо за вклад! 🎉
