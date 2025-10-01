# TITAN Analytics Platform - API Documentation

## 🎯 Новые Endpoints

### Категории шаблонов

```http
GET /api/v1/categories/
```
Получить список всех категорий шаблонов.

**Query Parameters:**
- `parent_only` (boolean) - Только родительские категории

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "Бизнес-аналитика",
      "slug": "business",
      "icon": "briefcase",
      "description": "Шаблоны для анализа рынков...",
      "parent": null,
      "position": 1,
      "subcategories": [],
      "templates_count": 5
    }
  ]
}
```

---

### Marketplace шаблонов

```http
GET /api/v1/marketplace/
```
Публичный маркетплейс шаблонов (доступен без авторизации).

**Query Parameters:**
- `search` (string) - Поиск по названию, описанию, тегам
- `category` (string) - Slug категории
- `premium` (boolean) - Только премиум шаблоны
- `ordering` (string) - Сортировка: `use_count`, `-rating`, `created_at`

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "Комплексный анализ рынка",
      "description": "Полный анализ целевого рынка...",
      "theme_name": "Рыночная аналитика",
      "category_name": "Бизнес-аналитика",
      "category_slug": "business",
      "tags": ["рынок", "аналитика"],
      "use_count": 150,
      "rating": 4.8,
      "is_premium": false,
      "author_name": "admin",
      "blocks_count": 5,
      "created_at": "2025-10-01T12:00:00Z"
    }
  ]
}
```

---

### Расширенная работа с шаблонами

#### Экспорт шаблона

```http
POST /api/v1/templates-extended/{id}/export/
```

Экспортирует шаблон в JSON формате для обмена.

**Response:**
```json
{
  "name": "Мой шаблон",
  "description": "Описание",
  "theme": "Название темы",
  "category": "category-slug",
  "tags": ["tag1", "tag2"],
  "meta_blocks": [
    {
      "query_template": "Запрос {theme}",
      "type": "plotly",
      "position": 0,
      "filters": {},
      "processing_params": {}
    }
  ],
  "version": "1.0",
  "exported_by": "TITAN Analytics Platform"
}
```

#### Импорт шаблона

```http
POST /api/v1/templates-extended/import/
```

Импортирует шаблон из JSON.

**Request Body:**
```json
{
  "name": "Импортированный шаблон",
  "description": "Описание",
  "theme": "Название темы",
  "category": "business",
  "tags": ["импорт", "тест"],
  "meta_blocks": [
    {
      "query_template": "Анализ {theme}",
      "type": "text",
      "position": 0,
      "filters": {},
      "processing_params": {}
    }
  ]
}
```

**Response:** 201 Created
```json
{
  "id": 10,
  "name": "Импортированный шаблон",
  ...
}
```

#### Избранное

```http
POST /api/v1/templates-extended/{id}/favorite/
```

Добавить/удалить шаблон из избранного.

**Response:**
```json
{
  "is_favorite": true,
  "message": "Добавлено в избранное"
}
```

#### Мои шаблоны

```http
GET /api/v1/templates-extended/my-templates/
```

Получить шаблоны, созданные текущим пользователем.

#### Избранные шаблоны

```http
GET /api/v1/templates-extended/favorites/
```

Получить избранные шаблоны пользователя.

---

### Источники данных

```http
GET /api/v1/data-sources/
```

Список доступных источников данных.

**Query Parameters:**
- `type` (string) - Фильтр по типу: `web`, `pdf`, `video`, `api`, etc.

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "Яндекс Поиск",
      "source_type": "web",
      "base_url": "https://yandex.ru",
      "api_key_required": true,
      "is_active": true,
      "config": {}
    }
  ]
}
```

---

### Пользовательские настройки

#### Получить настройки

```http
GET /api/v1/preferences/me/
```

Получить настройки текущего пользователя.

**Response:**
```json
{
  "id": 1,
  "user": 1,
  "favorite_templates": [1, 3, 5],
  "favorite_templates_details": [...],
  "default_theme": 2,
  "default_ai_model": "yandexgpt",
  "settings": {
    "notifications": true,
    "language": "ru"
  }
}
```

#### Обновить настройки

```http
PATCH /api/v1/preferences/{id}/
```

**Request Body:**
```json
{
  "default_ai_model": "yandexgpt-lite",
  "settings": {
    "notifications": false
  }
}
```

---

### Информация о процессорах

#### Список процессоров

```http
GET /api/v1/processors/list-processors/
```

Список всех зарегистрированных обработчиков данных.

**Response:**
```json
{
  "count": 6,
  "processors": [
    "SentimentAnalysisProcessor",
    "NetworkGraphProcessor",
    "TimelineProcessor",
    "ComparisonProcessor",
    "ForecastProcessor",
    "TableProcessor"
  ]
}
```

#### Типы блоков

```http
GET /api/v1/processors/block-types/
```

Доступные типы мета-блоков.

**Response:**
```json
{
  "types": [
    {"value": "plotly", "label": "Plotly"},
    {"value": "text", "label": "Текст"},
    {"value": "video", "label": "Видео"},
    {"value": "table", "label": "Таблица"},
    {"value": "map", "label": "Карта"},
    {"value": "timeline", "label": "Таймлайн"},
    {"value": "network", "label": "Граф связей"},
    {"value": "comparison", "label": "Сравнение"},
    {"value": "sentiment", "label": "Анализ тональности"},
    {"value": "forecast", "label": "Прогноз"}
  ]
}
```

---

## 🔐 Авторизация

Все endpoints (кроме `/marketplace/`) требуют авторизации через Token.

### Получить токен

```http
POST /api/v1/auth/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "token": "your_auth_token_here"
}
```

### Использование токена

```http
GET /api/v1/templates/
Authorization: Token your_auth_token_here
```

---

## 📊 Примеры использования

### Пример: Создание кастомного шаблона через API

```python
import requests

# 1. Авторизация
auth_response = requests.post(
    'http://localhost:8000/api/v1/auth/',
    json={'username': 'admin', 'password': 'password'}
)
token = auth_response.json()['token']
headers = {'Authorization': f'Token {token}'}

# 2. Создание шаблона
template_data = {
    'name': 'Мой аналитический отчёт',
    'description': 'Кастомный шаблон для моих нужд',
    'theme': 1,  # ID темы
    'category': 1,  # ID категории
    'tags': ['custom', 'analytics'],
    'is_public': False
}
response = requests.post(
    'http://localhost:8000/api/v1/templates-extended/',
    json=template_data,
    headers=headers
)
template_id = response.json()['id']

# 3. Добавление мета-блоков (через Django admin или напрямую в БД)

# 4. Экспорт шаблона для обмена
export_response = requests.post(
    f'http://localhost:8000/api/v1/templates-extended/{template_id}/export/',
    headers=headers
)
exported_template = export_response.json()

# Сохраняем в файл
with open('my_template.json', 'w') as f:
    json.dump(exported_template, f, indent=2)
```

### Пример: Поиск и использование публичного шаблона

```python
# 1. Поиск в Marketplace (без авторизации)
response = requests.get(
    'http://localhost:8000/api/v1/marketplace/',
    params={
        'category': 'business',
        'search': 'анализ рынка',
        'ordering': '-rating'
    }
)
templates = response.json()['results']

# 2. Добавление в избранное
template_id = templates[0]['id']
requests.post(
    f'http://localhost:8000/api/v1/templates-extended/{template_id}/favorite/',
    headers=headers
)

# 3. Создание отчёта на основе шаблона
report_data = {
    'template': template_id,
    'search_query_text': 'рынок металлургии',
    'search_start': '2024-01-01',
    'search_end': '2024-12-31'
}
report_response = requests.post(
    'http://localhost:8000/api/v1/report/',
    json=report_data,
    headers=headers
)
```

---

## 🚀 OpenAPI документация

Полная интерактивная документация доступна после запуска сервера:

- **Swagger UI**: http://localhost:8000/api/v1/swagger/
- **ReDoc**: http://localhost:8000/api/v1/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/v1/schema/
