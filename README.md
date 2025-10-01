## 🤝 Вклад в проект

Мы приветствуем ваш вклад в развитие TITAN Analytics Platform!

### Как помочь:

1. 🐛 Сообщайте о багах через Issues
2. 💡 Предлагайте новые фичи
3. 📝 Улучшайте документацию
4. 🔌 Создавайте новые процессоры данных
5. 📚 Делитесь шаблонами в Marketplace

### Процесс разработки:

```bash
# 1. Fork репозитория
# 2. Создайте ветку для фичи
git checkout -b feature/amazing-feature

# 3. Внесите изменения и commit
git commit -m 'Add amazing feature'

# 4. Push в ваш fork
git push origin feature/amazing-feature

# 5. Создайте Pull Request
```

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🙏 Благодарности

- [Yandex Cloud](https://cloud.yandex.ru/) за API для поиска и GPT
- [Django](https://www.djangoproject.com/) за отличный фреймворк
- [React](https://reactjs.org/) за мощный UI
- [Plotly](https://plotly.com/) за визуализацию
- Команде [Severstal ICT](https://github.com/NickScherbakov) за начальную реализацию

## 📞 Контакты

- **GitHub**: [NickScherbakov/Severstal_ICT2024](https://github.com/NickScherbakov/Severstal_ICT2024)
- **Issues**: [GitHub Issues](https://github.com/NickScherbakov/Severstal_ICT2024/issues)

---

<div align="center">

**Сделано с ❤️ командой TITAN Analytics**

⭐ Поставьте звезду, если проект был полезен!

</div>
````markdown
<div align="center">

# 🎯 TITAN Analytics Platform

**Универсальная платформа аналитики данных**

*Превращайте любые данные в действенные инсайты с помощью AI*

### 🌐 [**Посетите официальный сайт**](https://nickscherbakov.github.io/Severstal_ICT2024/) 🌐

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Website](https://img.shields.io/badge/🌐-Website-blue)](https://nickscherbakov.github.io/Severstal_ICT2024/)

</div>

---

## 📖 О проекте

**TITAN Analytics Platform** — это мощная универсальная платформа для сбора, анализа и визуализации данных из множества источников. Система объединяет возможности веб-скрейпинга, AI-обработки, интеллектуального поиска и генерации аналитических отчетов.

### ✨ Ключевые возможности

- 🔍 **Умный поиск** — семантический поиск с синонимами и ранжированием
- 🤖 **AI-анализ** — интеграция с YandexGPT для суммаризации и анализа
- 📊 **Визуализация** — интерактивные графики на Plotly
- 📝 **Отчёты** — экспорт в PDF, Word, Excel
- 🎬 **Мультимедиа** — анализ видео через субтитры YouTube
- 🔌 **Расширяемость** — модульная система обработчиков данных
- 📚 **Библиотека шаблонов** — готовые решения для типовых задач
- 🎨 **Конструктор отчётов** — визуальное создание кастомных аналитических отчётов

### 🎯 Use Cases

- **Бизнес-аналитика**: анализ рынка, конкурентная разведка, мониторинг цен
- **Медиа-мониторинг**: отслеживание репутации бренда, анализ упоминаний
- **Научные исследования**: обзор литературы, анализ публикаций
- **Юридический анализ**: мониторинг законодательства, судебная практика
- **Образование**: систематизация знаний, учебные материалы

## 🛠 Стек технологий

### Backend
- **Framework**: Python 3.11+ / Django 4.2
- **Database**: PostgreSQL 15
- **Task Queue**: Celery + RabbitMQ
- **Containerization**: Docker, docker-compose

### Data Processing
- **Analysis**: Pandas, NumPy
- **Web Scraping**: BeautifulSoup, Playwright
- **PDF Processing**: Pdfplumber, Camelot
- **NLP**: LangChain, RuWordNet, PyMorphy3
- **AI**: Yandex GPT API
- **Search**: Yandex Search API
- **Video**: YouTube API (поиск + субтитры)

### Frontend
- **Framework**: React 18 + TypeScript
- **Visualization**: Plotly.js
- **UI**: Tailwind CSS + Radix UI
- **State**: TanStack Query
- **Build**: Vite

### Infrastructure
- **Web Server**: Nginx
- **SSL**: Let's Encrypt
- **API Documentation**: DRF Spectacular (OpenAPI)

## 🏗 Архитектура

```
TITAN Analytics Platform
│
├── 🎨 Frontend (React + TypeScript)
│   ├── Конструктор отчётов
│   ├── Marketplace шаблонов
│   └── Интерактивная визуализация
│
├── ⚙️ Backend (Django REST API)
│   ├── 📊 Data Processing Pipeline
│   │   ├── Web Scraper
│   │   ├── PDF Parser
│   │   ├── Video Analyzer
│   │   └── File Processor
│   │
│   ├── 🤖 AI Processing Layer
│   │   ├── YandexGPT Integration
│   │   ├── Sentiment Analysis
│   │   ├── Entity Extraction
│   │   └── Summarization
│   │
│   ├── 🔍 Search Engine
│   │   ├── Semantic Search
│   │   ├── Synonym Expansion
│   │   └── Relevance Ranking
│   │
│   └── 🔌 Processor Registry
│       ├── Sentiment Processor
│       ├── Network Graph Processor
│       ├── Timeline Processor
│       ├── Forecast Processor
│       └── Custom Processors...
│
├── 💾 Data Layer
│   ├── PostgreSQL (structured data)
│   ├── File Storage (PDFs, media)
│   └── Search Index
│
└── ⚡ Task Queue (Celery + RabbitMQ)
    ├── Async data collection
    ├── Report generation
    └── Scheduled updates
```

## 🚀 Быстрый старт

### Запуск в продакшене (Docker)

1. **Клонировать репозиторий**

   ```bash
   git clone git@github.com:NickScherbakov/Severstal_ICT2024.git
   cd Severstal_ICT2024
   ```

2. **Настроить окружение**

   ```bash
   cp .env.example .env
   # Отредактируйте .env файл со своими настройками
   ```

3. **Настроить SSL (опционально)**

   Отредактируйте `init-letsencrypt.sh`:
   - Укажите ваш домен
   - Укажите email администратора
   
   ```bash
   chmod +x init-letsencrypt.sh
   ./init-letsencrypt.sh
   ```

4. **Запустить платформу**

   ```bash
   docker-compose up -d
   ```

   Платформа будет доступна по адресу: `https://ваш-домен.ru`

### Локальная разработка

#### 1. Подготовка окружения

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Копирование переменных окружения
cp .env.example .env
```

#### 2. Установка системных зависимостей (Linux)

```bash
# Для LangChain и Playwright
sudo apt-get install libwoff1 libwebpdemux2 libenchant-2-2 \
  libsecret-1-0 libhyphen0 libegl1 libevdev2 libgles2
```

#### 3. Запуск инфраструктуры

```bash
# Запуск PostgreSQL и RabbitMQ
docker-compose -f docker-compose-dev.yml up -d
```

#### 4. Установка Python зависимостей

```bash
cd backend
pip install -r requirements.txt

# Установка Playwright
playwright install
```

#### 5. Настройка базы данных

```bash
# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# 🎯 НОВОЕ: Загрузка библиотеки шаблонов TITAN
python manage.py load_template_library
```

#### 6. Инициализация поискового движка

```bash
# Скачивание RuWordNet для синонимов
ruwordnet download

# Парсинг начальных данных (настройте URL в файле)
# backend/accounts/management/commands/start_urls.py
python manage.py init_data

# Генерация поискового индекса
python generate_search.py search.pkl
```

#### 7. Запуск сервисов

```bash
# Терминал 1: Django dev server
python manage.py runserver

# Терминал 2: Celery worker
celery -A analyst worker -l info

# Терминал 3: Frontend (в другой директории)
cd ../titan_frontend
npm install
npm run dev
```

**🎉 Готово!** Платформа доступна:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000/api/`
- Admin: `http://localhost:8000/admin/`
- API Docs: `http://localhost:8000/api/schema/swagger-ui/`

## 🎯 Новые возможности TITAN Platform

### 📚 Библиотека шаблонов

Предустановленные шаблоны для типовых задач:

- **💼 Бизнес-аналитика**
  - Комплексный анализ рынка
  - Конкурентная разведка
  - Финансовая аналитика
  
- **🔬 Научные исследования**
  - Систематический обзор литературы
  - Анализ цитирований
  - Трендовый анализ публикаций

- **📺 Медиа-мониторинг**
  - Мониторинг репутации бренда
  - Анализ тональности упоминаний
  - Трекинг трендов

- **⚖️ Юридический анализ**
  - Мониторинг законодательства
  - Анализ судебной практики
  - Комплаенс-проверки

- **🎓 Образование**
  - Комплексное изучение темы
  - Систематизация знаний
  - Учебные обзоры

### 🔌 Система процессоров данных

TITAN использует модульную систему обработчиков:

- **Sentiment Analysis** — анализ тональности текста
- **Network Graph** — построение графов связей между сущностями
- **Timeline** — временные шкалы событий
- **Comparison** — сравнительный анализ
- **Forecast** — прогнозирование на основе данных
- **Table** — обработка табличных данных

**Легко расширяется!** Создайте свой процессор:

```python
from accounts.processors import DataProcessor, ProcessorRegistry

class MyCustomProcessor(DataProcessor):
    def can_process(self, block_type: str, data_type: str) -> bool:
        return block_type == 'my_type'
    
    def process(self, data, params):
        # Ваша логика обработки
        return {'type': 'my_type', 'result': ...}

# Регистрация
ProcessorRegistry.register(MyCustomProcessor())
```

### 🗂 Источники данных

Поддерживаемые источники:

- 🌐 Веб-страницы (HTML)
- 📄 PDF документы
- 🎬 Видео (YouTube с субтитрами)
- 📊 Файлы (CSV, Excel)
- 🔌 API endpoints
- 📰 Новостные агрегаторы
- 💬 Социальные сети (расширяемо)

### 🎨 Визуальный конструктор отчётов

Создавайте кастомные аналитические отчёты через UI:

1. Выберите категорию анализа
2. Добавьте нужные блоки (drag & drop)
3. Настройте фильтры и источники
4. Сохраните как шаблон
5. Поделитесь в Marketplace

## 📖 Документация API

После запуска сервера доступна интерактивная документация:

- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### Основные endpoints

```
GET    /api/v1/templates/          # Список шаблонов
GET    /api/v1/templates/marketplace/  # Публичные шаблоны
POST   /api/v1/templates/{id}/export/  # Экспорт шаблона
POST   /api/v1/templates/import/   # Импорт шаблона
GET    /api/v1/categories/         # Категории шаблонов
GET    /api/v1/reports/            # Список отчётов
POST   /api/v1/reports/            # Создать отчёт
GET    /api/v1/search/             # Поиск данных
```

## 🛠 Management команды

```bash
# Загрузка библиотеки шаблонов
python manage.py load_template_library

# Инициализация начальных данных
python manage.py init_data

# Индексация из CSV
python manage.py index_csv_file data.csv

# Экспорт моделей в CSV
python manage.py model2csv accounts.WebPage > pages.csv

# Генерация поискового индекса
python manage.py generate_search search.pkl
```

## 🔍 Поисковый движок

### Настройка продакшен-поиска

```bash
# 1. Скачивание RuWordNet для синонимов
ruwordnet download

# 2. Подготовка данных
python manage.py model2csv accounts.WebPage > pages.csv

# 3. Индексация
python manage.py index_csv_file pages.csv

# 4. Генерация поискового ресурса
python generate_search.py search.pkl
```

### Особенности поиска

- ✅ Семантический поиск с учётом синонимов (RuWordNet)
- ✅ Морфологический анализ (PyMorphy3)
- ✅ Ранжирование по релевантности
- ✅ Поддержка временных диапазонов
- ✅ Фильтрация по доменам
- ✅ Поиск по видео (через субтитры)
