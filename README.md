# 🏢 Organization Directory API

REST API для справочника организаций с информацией о зданиях и видах деятельности. Поддерживает геопоиск, рекурсивный поиск по дереву деятельностей и авторизацию через API ключ.

## 📋 Оглавление

- [Возможности](#-возможности)
- [Технологии](#-технологии)
- [Быстрый старт](#-быстрый-старт)
- [Установка](#-установка)
- [Использование](#-использование)
- [API Эндпоинты](#-api-эндпоинты)
- [Примеры запросов](#-примеры-запросов)
- [Docker](#-docker)
- [Разработка](#-разработка)
- [Устранение неполадок](-#устранение-неполадок)

## ✨ Возможности

- 📊 **Управление организациями** - CRUD операции для организаций
- 🏢 **Управление зданиями** - информация о зданиях с координатами
- 🎯 **Виды деятельности** - древовидная структура до 3 уровней вложенности
- 🔍 **Поиск** по названию, виду деятельности, местоположению
- 📍 **Геопоиск** в радиусе от заданной точки
- 📞 **Валидация телефонов** - поддержка российских форматов
- 🔐 **Авторизация** через API ключ
- 📚 **Документация** Swagger UI и ReDoc

## 🛠 Технологии

| Технология | Назначение |
|------------|------------|
| **FastAPI** | Веб-фреймворк для создания API |
| **SQLAlchemy** | ORM для работы с базой данных |
| **Alembic** | Миграции базы данных |
| **SQLite** | База данных (легковесная, не требует сервера) |
| **Pydantic** | Валидация данных и сериализация |
| **Docker** | Контейнеризация приложения |

## 🚀 Быстрый старт

### Способ 1: Локальный запуск

```bash
# 1. Клонирование репозитория
git clone <repository-url>
cd luna-org-directory-api-test

# 2. Установка зависимостей
pip install -e .

# 3. Применение миграций
python -m alembic upgrade head

# 4. Заполнение тестовыми данными
python data/seed_data.py 50

# 5. Запуск сервера
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Способ 2: Docker (рекомендуется)

```bash
# 1. Клонирование репозитория
git clone <repository-url>
cd luna-org-directory-api-test

# 2. Запуск в Docker
docker-compose up --build -d

# 3. Проверка работы
curl http://localhost:8000/
```

## 📦 Установка

### Требования
- Python 3.12+
- Docker (опционально)
- Git

### Шаги установки

1. **Клонирование репозитория**
```bash
git clone <repository-url>
cd luna-org-directory-api-test
```

2. **Создание виртуального окружения**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Установка зависимостей**
```bash
pip install -e .
```

4. **Настройка переменных окружения**
Создайте файл `.env` в корне проекта:
```env
API_KEY=your-secret-api-key
DATABASE_URL=sqlite:///./data/organizations.db
DEBUG=true
CORS_ORIGINS=["*"]
```

5. **Применение миграций**
```bash
python -m alembic upgrade head
```

6. **Заполнение тестовыми данными**
```bash
# 50 организаций
python data/seed_data.py 50

# 100 организаций
python data/seed_data.py 100
```

## 🎯 Использование

### Авторизация
Все запросы требуют API ключ в заголовке `Authorization: Bearer <API_KEY>`.
По умолчанию используется: `dev-api-key-12345`

### Базовые примеры

#### Получить список всех зданий
```bash
curl -H "Authorization: Bearer dev-api-key-12345" \
  http://localhost:8000/buildings/
```

#### Получить организации в конкретном здании
```bash
curl -H "Authorization: Bearer dev-api-key-12345" \
  http://localhost:8000/buildings/1/organizations
```

#### Получить дерево деятельностей
```bash
curl -H "Authorization: Bearer dev-api-key-12345" \
  http://localhost:8000/activities/
```

## 🔌 API Эндпоинты

### 📍 Здания
| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `GET` | `/buildings/` | Получить список всех зданий |
| `GET` | `/buildings/{id}/organizations` | Получить организации в конкретном здании |

### 🏢 Организации
| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `GET` | `/organizations/` | Получить список организаций с фильтрами |
| `GET` | `/organizations/{id}` | Получить информацию об организации |
| `GET` | `/organizations/?name={query}` | Поиск организаций по названию |
| `GET` | `/organizations/nearby?lat={lat}&lon={lon}&radius_km={radius}` | Геопоиск в радиусе |

### 🎯 Деятельность
| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `GET` | `/activities/` | Получить дерево видов деятельности |
| `GET` | `/activities/{id}/organizations` | Получить организации по виду деятельности |

## 📖 Примеры запросов

### Поиск организаций по названию
```bash
# Поиск по части названия
curl -H "Authorization: Bearer dev-api-key-12345" \
  "http://localhost:8000/organizations/?name=Рога"

# Ответ:
# [
#   {
#     "id": 1,
#     "name": "ООО Рога и Копыта",
#     "building": {
#       "id": 1,
#       "address": "г. Москва, ул. Ленина 1",
#       "latitude": 55.7558,
#       "longitude": 37.6173
#     },
#     "phone_numbers": ["+7 (495) 123-45-67", "+7 (495) 987-65-43"],
#     "activities": [{"id": 1, "name": "Еда"}, {"id": 2, "name": "Молочная продукция"}]
#   }
# ]
```

### Геопоиск в радиусе
```bash
# Поиск в радиусе 5 км от центра Москвы
curl -H "Authorization: Bearer dev-api-key-12345" \
  "http://localhost:8000/organizations/nearby?lat=55.7558&lon=37.6173&radius_km=5"
```

### Поиск по деятельности (рекурсивный)
```bash
# Поиск по "Еда" включает все дочерние категории
curl -H "Authorization: Bearer dev-api-key-12345" \
  "http://localhost:8000/activities/1/organizations"
```

### Получение организаций в здании
```bash
curl -H "Authorization: Bearer dev-api-key-12345" \
  "http://localhost:8000/buildings/1/organizations"
```

## 🐳 Docker

### Быстрый запуск
```bash
# Запуск в фоновом режиме
docker-compose up --build -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### Просмотр логов контейнера
```bash
docker-compose logs api
```

### Вход в контейнер
```bash
docker-compose exec api bash
```

## 🔧 Разработка

### Создание новой миграции
```bash
# Создание миграции после изменения моделей
python -m alembic revision --autogenerate -m "Add new field"

# Применение миграций
python -m alembic upgrade head

# Откат миграции
python -m alembic downgrade -1
```

### Форматирование кода
```bash
# Форматирование с помощью black
black app/

# Проверка типов (если используется mypy)
mypy app/
```

### Тестирование
```bash
# Запуск тестов
pytest

# Запуск с покрытием
pytest --cov=app tests/
```

## 🛠 Устранение неполадок

### Ошибка "Не удается подключиться к базе данных"
```bash
# Проверьте права на папку data
chmod 755 data/
# Или на Windows
icacls data /grant Everyone:F
```

### Ошибка "API ключ не найден"
```bash
# Убедитесь, что файл .env существует
cat .env
# Или задайте переменную окружения
export API_KEY=your-secret-key
```

### Ошибка Docker "port already in use"
```bash
# Проверьте занятые порты
netstat -tulpn | grep 8000
# Или используйте другой порт в docker-compose.yml
```

### Ошибка кодировки в Windows
```bash
# Установите кодировку UTF-8
set PYTHONIOENCODING=utf-8
```

## 📊 Структура ответов

### Формат ответа для организации
```json
{
  "id": 1,
  "name": "ООО Рога и Копыта",
  "building": {
    "id": 1,
    "address": "г. Москва, ул. Ленина 1",
    "latitude": 55.7558,
    "longitude": 37.6173
  },
  "phone_numbers": ["+7 (495) 123-45-67", "+7 (495) 987-65-43"],
  "activities": [
    {"id": 1, "name": "Еда"},
    {"id": 2, "name": "Молочная продукция"}
  ]
}
```

### Формат ответа для здания
```json
{
  "id": 1,
  "address": "г. Москва, ул. Ленина 1",
  "latitude": 55.7558,
  "longitude": 37.6173
}
```

### Формат ответа для деятельности
```json
{
  "id": 1,
  "name": "Еда",
  "parent_id": null,
  "level": 1,
  "children": [
    {
      "id": 2,
      "name": "Молочная продукция",
      "parent_id": 1,
      "level": 2,
      "children": []
    }
  ]
}
```

## 📚 Документация

После запуска сервера документация доступна по адресам:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
