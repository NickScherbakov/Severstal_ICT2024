# 🚀 TITAN Analytics Platform - Upgrade Guide

## Краткая инструкция по обновлению до версии 1.0.0

---

## ⚡ Быстрое обновление (5 минут)

### Для продакшен-сервера (Docker)

```bash
# 1. Остановка контейнеров
docker-compose down

# 2. Обновление кода
git pull origin master

# 3. Пересборка и запуск
docker-compose up -d --build

# 4. Применение миграций (внутри контейнера)
docker-compose exec backend python manage.py migrate

# 5. Загрузка библиотеки шаблонов (опционально)
docker-compose exec backend python manage.py load_template_library

# Готово! 🎉
```

### Для локальной разработки

```bash
# 1. Обновление кода
git pull origin master

# 2. Обновление зависимостей (если были изменения)
cd backend
pip install -r requirements.txt

# 3. Применение миграций
python manage.py migrate

# 4. Загрузка библиотеки шаблонов
python manage.py load_template_library

# 5. Обновление фронтенда
cd ../titan_frontend
npm install
npm run build  # или npm run dev для разработки

# 6. Перезапуск сервисов
# Django: Ctrl+C и снова python manage.py runserver
# Celery: Ctrl+C и снова celery -A analyst worker -l info

# Готово! 🎉
```

---

## 📋 Что нового?

### ✨ Главные фичи

1. **7 новых типов блоков** - table, map, timeline, network, comparison, sentiment, forecast
2. **Библиотека шаблонов** - 6+ готовых шаблонов для разных задач
3. **Marketplace** - публичный каталог шаблонов
4. **Система процессоров** - модульная обработка данных с AI
5. **Категории шаблонов** - структурированная организация
6. **Экспорт/Импорт** - обмен шаблонами между пользователями
7. **Пользовательские настройки** - избранное, предпочтения

### 🌐 Новые API endpoints

```
GET    /api/v1/categories/              # Категории
GET    /api/v1/marketplace/             # Публичные шаблоны
POST   /api/v1/templates-extended/{id}/export/  # Экспорт
POST   /api/v1/templates-extended/import/       # Импорт
GET    /api/v1/data-sources/            # Источники данных
GET    /api/v1/preferences/me/          # Настройки
GET    /api/v1/processors/list-processors/  # Процессоры
```

Полная документация: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## ✅ Проверка работоспособности

### После обновления проверьте:

1. **Миграции применены:**
   ```bash
   python manage.py showmigrations accounts
   # Должна быть [X] 0012_titan_platform_extensions
   ```

2. **Шаблоны загружены:**
   ```bash
   python manage.py shell
   >>> from accounts.models import Template, TemplateCategory
   >>> Template.objects.count()  # Должно быть > 0
   >>> TemplateCategory.objects.count()  # Должно быть 5
   ```

3. **API работает:**
   ```bash
   curl http://localhost:8000/api/v1/marketplace/
   # Должен вернуть JSON с шаблонами
   ```

4. **Процессоры инициализированы:**
   ```bash
   python manage.py shell
   >>> from accounts.processors import ProcessorRegistry
   >>> ProcessorRegistry.list_processors()
   # Должно быть 6 процессоров
   ```

---

## 🔧 Настройка после обновления

### Рекомендуемые действия:

#### 1. Назначьте категории существующим шаблонам

Зайдите в админку: `/admin/accounts/template/`

Для каждого старого шаблона:
- Выберите подходящую категорию
- Заполните description
- Добавьте tags
- При желании сделайте `is_public=True` для Marketplace

#### 2. Настройте источники данных

Зайдите в админку: `/admin/accounts/datasource/`

Проверьте и при необходимости настройте:
- Яндекс Поиск (api_key из settings)
- YouTube
- Другие источники

#### 3. Создайте свой первый шаблон TITAN

```python
# В Django shell
from accounts.models import *

# Создание темы
theme = Theme.objects.create(name="Моя тема")

# Получение категории
category = TemplateCategory.objects.get(slug='business')

# Создание шаблона
template = Template.objects.create(
    name="Мой первый TITAN шаблон",
    description="Тестовый шаблон",
    theme=theme,
    category=category,
    tags=['test', 'custom'],
    is_public=False
)

# Добавление блоков
MetaBlock.objects.create(
    query_template="Анализ тональности {theme}",
    template=template,
    type='sentiment',
    position=0,
    processing_params={'model': 'yandexgpt'}
)

MetaBlock.objects.create(
    query_template="Граф связей {theme}",
    template=template,
    type='network',
    position=1
)

print(f"✅ Шаблон создан: {template.id}")
```

#### 4. Протестируйте новые процессоры

```python
from accounts.processors import ProcessorRegistry

# Получаем процессор для анализа тональности
processor = ProcessorRegistry.get_processor('sentiment')

# Тестовые данные
test_data = {
    'data': 'Отличный продукт! Очень доволен покупкой.'
}

# Обработка
result = processor.process(test_data, {'model': 'yandexgpt'})
print(result)
```

---

## 🐛 Возможные проблемы

### Проблема: Миграция не применяется

```bash
# Решение 1: Fake миграция если БД уже обновлена
python manage.py migrate accounts 0012_titan_platform_extensions --fake

# Решение 2: Пересоздание миграций
python manage.py migrate accounts 0011_reportblock_representation
python manage.py migrate accounts 0012_titan_platform_extensions
```

### Проблема: Import ошибка в views_extended

```bash
# Убедитесь что processors.py существует
ls backend/accounts/processors.py

# Проверьте импорты в Python shell
python manage.py shell
>>> from accounts.processors import ProcessorRegistry
>>> # Должно работать без ошибок
```

### Проблема: 404 на новых endpoints

```bash
# Проверьте что urls.py импортирует views_extended
grep "views_extended" backend/api/v1/urls.py

# Перезапустите сервер
python manage.py runserver
```

### Проблема: Процессоры не работают

```python
# В Django shell проверьте инициализацию
from accounts.processors import ProcessorRegistry
ProcessorRegistry._initialized  # Должно быть True
len(ProcessorRegistry._processors)  # Должно быть 6
```

---

## 📚 Дополнительные ресурсы

- **Полный CHANGELOG**: [CHANGELOG.md](./CHANGELOG.md)
- **API документация**: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **README**: [README.md](./README.md)
- **GitHub Issues**: https://github.com/NickScherbakov/Severstal_ICT2024/issues

---

## 🎉 Поздравляем!

Теперь у вас работает **TITAN Analytics Platform v1.0.0** - универсальная платформа для аналитики с AI! 

### Что дальше?

1. 📚 Изучите [библиотеку шаблонов](./README.md#-библиотека-шаблонов)
2. 🔧 Создайте свой кастомный процессор
3. 📊 Постройте свой первый отчёт с новыми типами блоков
4. 🌐 Поделитесь шаблонами в Marketplace
5. ⭐ Поставьте звезду на GitHub!

---

**Нужна помощь?** Создайте [Issue](https://github.com/NickScherbakov/Severstal_ICT2024/issues) или посмотрите [Discussions](https://github.com/NickScherbakov/Severstal_ICT2024/discussions)

**Happy Analyzing!** 🎯✨
