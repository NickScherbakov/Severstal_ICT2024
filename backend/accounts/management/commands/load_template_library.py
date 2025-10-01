"""
TITAN Analytics Platform - Template Library Loader
Загружает предустановленную библиотеку шаблонов для различных use-cases
"""

from django.core.management.base import BaseCommand
from accounts.models import Theme, Template, MetaBlock, TemplateCategory, DataSource


class Command(BaseCommand):
    help = 'Загружает библиотеку готовых шаблонов TITAN Analytics Platform'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Начинаем загрузку библиотеки шаблонов TITAN Analytics...'))
        
        # Создаем источники данных
        self._create_data_sources()
        
        # Создаем категории
        categories = self._create_categories()
        
        # Создаем шаблоны для каждой категории
        self._create_business_templates(categories['business'])
        self._create_research_templates(categories['research'])
        self._create_media_templates(categories['media'])
        self._create_legal_templates(categories['legal'])
        self._create_education_templates(categories['education'])
        
        self.stdout.write(self.style.SUCCESS('✅ Библиотека шаблонов успешно загружена!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Всего категорий: {TemplateCategory.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📋 Всего шаблонов: {Template.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'🔧 Всего мета-блоков: {MetaBlock.objects.count()}'))

    def _create_data_sources(self):
        """Создает стандартные источники данных"""
        self.stdout.write('📡 Создание источников данных...')
        
        sources = [
            {
                'name': 'Яндекс Поиск',
                'source_type': 'web',
                'base_url': 'https://yandex.ru',
                'api_key_required': True,
                'is_active': True,
            },
            {
                'name': 'YouTube',
                'source_type': 'video',
                'base_url': 'https://youtube.com',
                'api_key_required': False,
                'is_active': True,
            },
            {
                'name': 'Центральный Банк РФ',
                'source_type': 'web',
                'base_url': 'https://cbr.ru',
                'api_key_required': False,
                'is_active': True,
            },
            {
                'name': 'Росстат',
                'source_type': 'web',
                'base_url': 'https://rosstat.gov.ru',
                'api_key_required': False,
                'is_active': True,
            },
            {
                'name': 'Пользовательские файлы',
                'source_type': 'file',
                'api_key_required': False,
                'is_active': True,
            },
        ]
        
        for source_data in sources:
            DataSource.objects.get_or_create(
                name=source_data['name'],
                defaults=source_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Создано источников: {DataSource.objects.count()}'))

    def _create_categories(self):
        """Создает категории шаблонов"""
        self.stdout.write('📂 Создание категорий...')
        
        categories = {}
        
        cat_data = [
            {
                'name': 'Бизнес-аналитика',
                'slug': 'business',
                'icon': 'briefcase',
                'description': 'Шаблоны для анализа рынков, конкурентов, финансовой отчетности',
                'position': 1,
            },
            {
                'name': 'Научные исследования',
                'slug': 'research',
                'icon': 'flask',
                'description': 'Анализ публикаций, цитирований, научных трендов',
                'position': 2,
            },
            {
                'name': 'Медиа-мониторинг',
                'slug': 'media',
                'icon': 'tv',
                'description': 'Отслеживание упоминаний, репутации, медиа-трендов',
                'position': 3,
            },
            {
                'name': 'Юридический анализ',
                'slug': 'legal',
                'icon': 'gavel',
                'description': 'Мониторинг законодательства, судебной практики',
                'position': 4,
            },
            {
                'name': 'Образование',
                'slug': 'education',
                'icon': 'graduation-cap',
                'description': 'Учебные материалы, курсы, базы знаний',
                'position': 5,
            },
        ]
        
        for cat in cat_data:
            category, created = TemplateCategory.objects.get_or_create(
                slug=cat['slug'],
                defaults=cat
            )
            categories[cat['slug']] = category
            status = '✓ создана' if created else '≈ существует'
            self.stdout.write(f'  {status}: {cat["name"]}')
        
        return categories

    def _create_business_templates(self, category):
        """Создает шаблоны для бизнес-аналитики"""
        self.stdout.write('💼 Создание бизнес-шаблонов...')
        
        # Шаблон: Комплексный анализ рынка
        theme, _ = Theme.objects.get_or_create(name='Рыночная аналитика')
        template, created = Template.objects.get_or_create(
            name='Комплексный анализ рынка',
            defaults={
                'theme': theme,
                'category': category,
                'description': 'Полный анализ целевого рынка: объем, динамика, игроки, тренды',
                'is_public': True,
                'tags': ['рынок', 'аналитика', 'объем', 'тренды'],
            }
        )
        
        if created:
            blocks_data = [
                ('Объем и динамика рынка {theme}', MetaBlock.PLOTLY, {'chart_type': 'line'}),
                ('Ключевые игроки рынка {theme}', MetaBlock.TABLE, {}),
                ('Тренды и прогнозы развития {theme}', MetaBlock.FORECAST, {'model': 'yandexgpt'}),
                ('Регуляторная среда {theme}', MetaBlock.TEXT, {}),
                ('SWOT-анализ рынка {theme}', MetaBlock.COMPARISON, {'items': ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']}),
            ]
            
            for i, (query, block_type, params) in enumerate(blocks_data):
                MetaBlock.objects.create(
                    query_template=query,
                    template=template,
                    type=block_type,
                    position=i,
                    processing_params=params
                )
            
            self.stdout.write(f'  ✓ {template.name}')
        
        # Шаблон: Конкурентная разведка
        theme, _ = Theme.objects.get_or_create(name='Конкурентный анализ')
        template, created = Template.objects.get_or_create(
            name='Конкурентная разведка',
            defaults={
                'theme': theme,
                'category': category,
                'description': 'Детальный анализ конкурентов и их стратегий',
                'is_public': True,
                'tags': ['конкуренты', 'стратегия', 'позиционирование'],
            }
        )
        
        if created:
            blocks_data = [
                ('Список основных конкурентов {theme}', MetaBlock.TABLE, {}),
                ('Сравнительный анализ продуктов {theme}', MetaBlock.COMPARISON, {}),
                ('Карта позиционирования {theme}', MetaBlock.PLOTLY, {'chart_type': 'scatter'}),
                ('Финансовые показатели конкурентов {theme}', MetaBlock.TABLE, {}),
                ('Анализ стратегий конкурентов {theme}', MetaBlock.TEXT, {}),
                ('Прогноз действий конкурентов {theme}', MetaBlock.FORECAST, {}),
            ]
            
            for i, (query, block_type, params) in enumerate(blocks_data):
                MetaBlock.objects.create(
                    query_template=query,
                    template=template,
                    type=block_type,
                    position=i,
                    processing_params=params
                )
            
            self.stdout.write(f'  ✓ {template.name}')

    def _create_research_templates(self, category):
        """Создает шаблоны для научных исследований"""
        self.stdout.write('🔬 Создание научных шаблонов...')
        
        # Шаблон: Обзор литературы
        theme, _ = Theme.objects.get_or_create(name='Научный обзор')
        template, created = Template.objects.get_or_create(
            name='Систематический обзор литературы',
            defaults={
                'theme': theme,
                'category': category,
                'description': 'Анализ научных публикаций по теме исследования',
                'is_public': True,
                'tags': ['наука', 'публикации', 'обзор', 'цитирование'],
            }
        )
        
        if created:
            blocks_data = [
                ('Ключевые публикации по теме {theme}', MetaBlock.TABLE, {}),
                ('Временная динамика публикаций {theme}', MetaBlock.TIMELINE, {}),
                ('Наиболее цитируемые работы {theme}', MetaBlock.TABLE, {}),
                ('Сеть соавторства {theme}', MetaBlock.NETWORK, {}),
                ('Основные направления исследований {theme}', MetaBlock.TEXT, {}),
                ('Перспективные направления {theme}', MetaBlock.FORECAST, {}),
            ]
            
            for i, (query, block_type, params) in enumerate(blocks_data):
                MetaBlock.objects.create(
                    query_template=query,
                    template=template,
                    type=block_type,
                    position=i,
                    processing_params=params
                )
            
            self.stdout.write(f'  ✓ {template.name}')

    def _create_media_templates(self, category):
        """Создает шаблоны для медиа-мониторинга"""
        self.stdout.write('📺 Создание медиа-шаблонов...')
        
        # Шаблон: Репутационный анализ
        theme, _ = Theme.objects.get_or_create(name='Медиа-аналитика')
        template, created = Template.objects.get_or_create(
            name='Мониторинг репутации бренда',
            defaults={
                'theme': theme,
                'category': category,
                'description': 'Отслеживание упоминаний и анализ репутации в медиа',
                'is_public': True,
                'tags': ['репутация', 'бренд', 'упоминания', 'тональность'],
            }
        )
        
        if created:
            blocks_data = [
                ('Все упоминания бренда {theme}', MetaBlock.TEXT, {}),
                ('Анализ тональности упоминаний {theme}', MetaBlock.SENTIMENT, {}),
                ('Динамика упоминаний {theme}', MetaBlock.TIMELINE, {}),
                ('Ключевые темы обсуждений {theme}', MetaBlock.TEXT, {}),
                ('Видео-упоминания {theme}', MetaBlock.VIDEO, {}),
                ('Рекомендации по улучшению {theme}', MetaBlock.TEXT, {}),
            ]
            
            for i, (query, block_type, params) in enumerate(blocks_data):
                MetaBlock.objects.create(
                    query_template=query,
                    template=template,
                    type=block_type,
                    position=i,
                    processing_params=params
                )
            
            self.stdout.write(f'  ✓ {template.name}')

    def _create_legal_templates(self, category):
        """Создает шаблоны для юридического анализа"""
        self.stdout.write('⚖️ Создание юридических шаблонов...')
        
        # Шаблон: Законодательный мониторинг
        theme, _ = Theme.objects.get_or_create(name='Правовой анализ')
        template, created = Template.objects.get_or_create(
            name='Мониторинг законодательства',
            defaults={
                'theme': theme,
                'category': category,
                'description': 'Отслеживание изменений в законодательстве',
                'is_public': True,
                'tags': ['законы', 'регулирование', 'комплаенс'],
            }
        )
        
        if created:
            blocks_data = [
                ('Изменения в законодательстве {theme}', MetaBlock.TIMELINE, {}),
                ('Новые нормативные акты {theme}', MetaBlock.TABLE, {}),
                ('Анализ влияния на бизнес {theme}', MetaBlock.TEXT, {}),
                ('Сравнение с международной практикой {theme}', MetaBlock.COMPARISON, {}),
                ('Рекомендации по адаптации {theme}', MetaBlock.TEXT, {}),
            ]
            
            for i, (query, block_type, params) in enumerate(blocks_data):
                MetaBlock.objects.create(
                    query_template=query,
                    template=template,
                    type=block_type,
                    position=i,
                    processing_params=params
                )
            
            self.stdout.write(f'  ✓ {template.name}')

    def _create_education_templates(self, category):
        """Создает шаблоны для образования"""
        self.stdout.write('🎓 Создание образовательных шаблонов...')
        
        # Шаблон: Учебный обзор
        theme, _ = Theme.objects.get_or_create(name='Образование')
        template, created = Template.objects.get_or_create(
            name='Комплексное изучение темы',
            defaults={
                'theme': theme,
                'category': category,
                'description': 'Систематизация знаний по учебной теме',
                'is_public': True,
                'tags': ['обучение', 'знания', 'материалы'],
            }
        )
        
        if created:
            blocks_data = [
                ('Теоретический обзор {theme}', MetaBlock.TEXT, {}),
                ('Ключевые концепции {theme}', MetaBlock.TABLE, {}),
                ('Исторический контекст {theme}', MetaBlock.TIMELINE, {}),
                ('Связи между концепциями {theme}', MetaBlock.NETWORK, {}),
                ('Видео-лекции по теме {theme}', MetaBlock.VIDEO, {}),
                ('Практические примеры {theme}', MetaBlock.TEXT, {}),
            ]
            
            for i, (query, block_type, params) in enumerate(blocks_data):
                MetaBlock.objects.create(
                    query_template=query,
                    template=template,
                    type=block_type,
                    position=i,
                    processing_params=params
                )
            
            self.stdout.write(f'  ✓ {template.name}')
