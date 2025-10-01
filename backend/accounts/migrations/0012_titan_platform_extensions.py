# Generated manually for TITAN Analytics Platform
# Date: 2025-10-01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0011_reportblock_representation'),
    ]

    operations = [
        # Создание новых моделей
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('source_type', models.CharField(choices=[('web', 'Веб-страница'), ('pdf', 'PDF документ'), ('video', 'Видео'), ('api', 'API'), ('database', 'База данных'), ('file', 'Файл (CSV/Excel)'), ('social', 'Социальные сети'), ('news', 'Новостные агрегаторы')], max_length=20, verbose_name='Тип источника')),
                ('base_url', models.URLField(blank=True, verbose_name='Базовый URL')),
                ('api_key_required', models.BooleanField(default=False, verbose_name='Требуется API ключ')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('config', models.JSONField(blank=True, default=dict, verbose_name='Конфигурация')),
            ],
            options={
                'verbose_name': 'Источник данных',
                'verbose_name_plural': 'Источники данных',
            },
        ),
        migrations.CreateModel(
            name='TemplateCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('icon', models.CharField(blank=True, max_length=50, verbose_name='Иконка')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='Позиция')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='accounts.templatecategory', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория шаблона',
                'verbose_name_plural': 'Категории шаблонов',
                'ordering': ['position', 'name'],
            },
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_ai_model', models.CharField(choices=[('yandexgpt', 'YandexGPT'), ('yandexgpt-lite', 'YandexGPT Lite')], default='yandexgpt', max_length=50, verbose_name='AI модель по умолчанию')),
                ('settings', models.JSONField(blank=True, default=dict, verbose_name='Настройки')),
                ('default_theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.theme', verbose_name='Тематика по умолчанию')),
                ('favorite_templates', models.ManyToManyField(blank=True, related_name='favorited_by', to='accounts.template', verbose_name='Избранные шаблоны')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользовательские настройки',
                'verbose_name_plural': 'Пользовательские настройки',
            },
        ),
        
        # Расширение существующих моделей
        # Добавление новых типов в MetaBlock
        migrations.AlterField(
            model_name='metablock',
            name='type',
            field=models.CharField(choices=[('plotly', 'Plotly'), ('text', 'Текст'), ('video', 'Видео'), ('table', 'Таблица'), ('map', 'Карта'), ('timeline', 'Таймлайн'), ('network', 'Граф связей'), ('comparison', 'Сравнение'), ('sentiment', 'Анализ тональности'), ('forecast', 'Прогноз')], verbose_name='Тип'),
        ),
        
        # Добавление новых полей в MetaBlock
        migrations.AddField(
            model_name='metablock',
            name='filters',
            field=models.JSONField(blank=True, default=dict, help_text='JSON с настройками фильтрации (домены, даты, языки и т.д.)', verbose_name='Фильтры'),
        ),
        migrations.AddField(
            model_name='metablock',
            name='processing_params',
            field=models.JSONField(blank=True, default=dict, help_text='Параметры для AI/ML обработки', verbose_name='Параметры обработки'),
        ),
        migrations.AddField(
            model_name='metablock',
            name='data_sources',
            field=models.ManyToManyField(blank=True, to='accounts.datasource', verbose_name='Источники данных'),
        ),
        
        # Добавление новых полей в Template
        migrations.AddField(
            model_name='template',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='templates', to='accounts.templatecategory', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='template',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='template',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='Публичный'),
        ),
        migrations.AddField(
            model_name='template',
            name='is_premium',
            field=models.BooleanField(default=False, verbose_name='Премиум'),
        ),
        migrations.AddField(
            model_name='template',
            name='tags',
            field=models.JSONField(blank=True, default=list, verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='template',
            name='use_count',
            field=models.IntegerField(default=0, verbose_name='Количество использований'),
        ),
        migrations.AddField(
            model_name='template',
            name='rating',
            field=models.FloatField(default=0.0, verbose_name='Рейтинг'),
        ),
        migrations.AddField(
            model_name='template',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_templates', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='template',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True),
        ),
    ]
