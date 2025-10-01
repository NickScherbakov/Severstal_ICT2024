# 🎯 TITAN Analytics Platform - Quick Start

**5-минутный старт с примерами!**

---

## 🚀 Запуск (выберите один способ)

### Вариант 1: Docker (рекомендуется)

```bash
git clone https://github.com/NickScherbakov/Severstal_ICT2024.git
cd Severstal_ICT2024
cp .env.example .env

docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py load_template_library

# Готово! Открывайте http://localhost:8000
```

### Вариант 2: Локально

```bash
git clone https://github.com/NickScherbakov/Severstal_ICT2024.git
cd Severstal_ICT2024/backend

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
docker-compose -f docker-compose-dev.yml up -d  # БД и RabbitMQ

python manage.py migrate
python manage.py createsuperuser
python manage.py load_template_library

python manage.py runserver
# Открывайте http://localhost:8000
```

---

## 📚 Первые шаги

### 1️⃣ Изучите Marketplace

```bash
curl http://localhost:8000/api/v1/marketplace/
```

Или откройте в браузере: http://localhost:8000/api/v1/swagger/

### 2️⃣ Получите токен авторизации

```bash
curl -X POST http://localhost:8000/api/v1/auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"ваш_пароль"}'
```

Сохраните токен:
```json
{"token":"a1b2c3d4e5f6..."}
```

### 3️⃣ Создайте свой первый отчёт

```bash
TOKEN="ваш_токен"

# Список шаблонов
curl http://localhost:8000/api/v1/template/ \
  -H "Authorization: Token $TOKEN"

# Создание отчёта
curl -X POST http://localhost:8000/api/v1/report/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "template": 1,
    "search_query_text": "искусственный интеллект",
    "search_start": "2024-01-01",
    "search_end": "2024-12-31"
  }'
```

---

## 💡 Примеры использования

### Пример 1: Анализ рынка

```python
import requests

# Авторизация
response = requests.post(
    'http://localhost:8000/api/v1/auth/',
    json={'username': 'admin', 'password': 'password'}
)
token = response.json()['token']
headers = {'Authorization': f'Token {token}'}

# Поиск шаблона "Анализ рынка"
templates = requests.get(
    'http://localhost:8000/api/v1/marketplace/',
    params={'search': 'анализ рынка'}
).json()

template_id = templates['results'][0]['id']

# Создание отчёта
report = requests.post(
    'http://localhost:8000/api/v1/report/',
    json={
        'template': template_id,
        'search_query_text': 'рынок металлургии 2024',
        'search_start': '2024-01-01',
        'search_end': '2024-10-01'
    },
    headers=headers
).json()

print(f"Отчёт создан: {report['id']}")
```

### Пример 2: Создание кастомного шаблона

```python
from accounts.models import *

# Тема
theme = Theme.objects.create(name="Конкурентный анализ")

# Категория
category = TemplateCategory.objects.get(slug='business')

# Шаблон
template = Template.objects.create(
    name="Мониторинг конкурентов",
    description="Отслеживание действий конкурентов",
    theme=theme,
    category=category,
    tags=['конкуренты', 'мониторинг'],
    is_public=True
)

# Блоки
blocks = [
    ("Список конкурентов {theme}", "table", 0),
    ("Анализ тональности упоминаний {theme}", "sentiment", 1),
    ("График динамики {theme}", "plotly", 2),
    ("Прогноз действий {theme}", "forecast", 3),
]

for query, block_type, pos in blocks:
    MetaBlock.objects.create(
        query_template=query,
        template=template,
        type=block_type,
        position=pos
    )

print(f"✅ Шаблон готов! ID: {template.id}")
```

### Пример 3: Использование процессоров

```python
from accounts.processors import ProcessorRegistry

# Анализ тональности
sentiment_processor = ProcessorRegistry.get_processor('sentiment')
result = sentiment_processor.process(
    data={'data': 'Отличный продукт, всем рекомендую!'},
    params={'model': 'yandexgpt'}
)
print(result)

# Граф связей
network_processor = ProcessorRegistry.get_processor('network')
result = network_processor.process(
    data={'data': 'Apple купила стартап Acme. CEO John Smith стал VP.'},
    params={}
)
print(result['graph_data'])
```

### Пример 4: Экспорт/Импорт шаблонов

```python
import json
import requests

# Экспорт
export = requests.post(
    f'http://localhost:8000/api/v1/templates-extended/1/export/',
    headers=headers
).json()

# Сохранение в файл
with open('my_template.json', 'w', encoding='utf-8') as f:
    json.dump(export, f, ensure_ascii=False, indent=2)

# Импорт на другом сервере
with open('my_template.json', 'r', encoding='utf-8') as f:
    template_data = json.load(f)

imported = requests.post(
    'http://another-server.com/api/v1/templates-extended/import/',
    json=template_data,
    headers=headers
).json()

print(f"Импортирован: {imported['id']}")
```

---

## 🎨 Доступные типы блоков

| Тип | Описание | Пример использования |
|-----|----------|---------------------|
| `plotly` | Графики | Динамика цен, объемы |
| `text` | Текст | Описания, выводы |
| `video` | Видео | YouTube обзоры |
| `table` | Таблица | Списки, сравнения |
| `map` | Карта | Географические данные |
| `timeline` | Таймлайн | Хронология событий |
| `network` | Граф | Связи между компаниями |
| `comparison` | Сравнение | SWOT, конкуренты |
| `sentiment` | Тональность | Анализ отзывов |
| `forecast` | Прогноз | Предсказания трендов |

---

## 📊 Готовые шаблоны

После `load_template_library` доступны:

### 💼 Бизнес
- **Комплексный анализ рынка** - объем, игроки, тренды, SWOT
- **Конкурентная разведка** - сравнение, стратегии, прогнозы

### 🔬 Наука
- **Систематический обзор литературы** - публикации, цитирование, тренды

### 📺 Медиа
- **Мониторинг репутации бренда** - упоминания, тональность, динамика

### ⚖️ Право
- **Мониторинг законодательства** - изменения, влияние, рекомендации

### 🎓 Образование
- **Комплексное изучение темы** - теория, концепции, примеры

---

## 🛠 Полезные команды

```bash
# Просмотр всех шаблонов
python manage.py shell
>>> from accounts.models import Template
>>> for t in Template.objects.all(): print(t.id, t.name)

# Экспорт данных
python manage.py model2csv accounts.Template > templates.csv

# Генерация поискового индекса
python generate_search.py search.pkl

# Запуск Celery worker
celery -A analyst worker -l info

# Просмотр процессоров
python manage.py shell
>>> from accounts.processors import ProcessorRegistry
>>> ProcessorRegistry.list_processors()
```

---

## 📖 Документация

- **Полная документация**: [README.md](./README.md)
- **API Reference**: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Список изменений**: [CHANGELOG.md](./CHANGELOG.md)
- **Обновление**: [UPGRADE_GUIDE.md](./UPGRADE_GUIDE.md)
- **Swagger UI**: http://localhost:8000/api/v1/swagger/

---

## 🎯 Следующие шаги

1. ✅ Изучите готовые шаблоны в Marketplace
2. ✅ Создайте свой первый отчёт
3. ✅ Настройте избранные шаблоны
4. ✅ Экспериментируйте с процессорами
5. ✅ Создайте кастомный шаблон под свои задачи
6. ✅ Поделитесь результатом в Issues!

---

## ❓ FAQ

**Q: Где найти API токен?**  
A: `POST /api/v1/auth/` с username/password

**Q: Как добавить новый тип обработки?**  
A: Создайте класс наследующий `DataProcessor` и зарегистрируйте через `ProcessorRegistry.register()`

**Q: Можно ли использовать без YandexGPT?**  
A: Да, но некоторые процессоры (sentiment, network) требуют AI модель

**Q: Как экспортировать отчёт?**  
A: `POST /api/v1/report/{id}/download_report/` с параметром `type=pdf|msword|excel`

**Q: Есть ли ограничения на количество шаблонов?**  
A: Нет, создавайте сколько нужно!

---

## 🆘 Помощь

- 📝 [GitHub Issues](https://github.com/NickScherbakov/Severstal_ICT2024/issues)
- 💬 [Discussions](https://github.com/NickScherbakov/Severstal_ICT2024/discussions)
- 📚 [Full Documentation](./README.md)

---

**Готовы к аналитике? Вперёд!** 🚀🎯

⭐ Не забудьте поставить звезду проекту на GitHub!
