from datetime import date
import pickle
from django.db import models
from django.db.transaction import atomic
from django.forms import model_to_dict
from extract.process_df import preprocess_entity
from search import ya_search, find_youtube_video
from analyst.settings import BASE_DIR, YANDEX_SEARCH_API_TOKEN
from rest_framework import serializers
import markdown

from accounts.models import (
    WebPage, Data, MetaBlock, Report,
    ReportBlock, SearchQuery, Template, Theme
)
from accounts.tasks import add_data_to_report_block, add_video_data_to_report_block, add_search_data_to_report_block
from extract.reports import get_one_figure_by_entity


search_engine = None
try:
    search_engine = pickle.load(open(f'{BASE_DIR}/search.pkl', 'rb'))
except FileNotFoundError:
    print('No search.pkl file found')


class DataSearchSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    snippet = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Data
        fields = (
            'id',
            'name',
            'type',
            'url',
            'snippet'
        )

    def get_snippet(self, obj):
        return 'Пример сниппета'

    def get_name(self, obj):
        return obj.name

    def get_url(self, obj):
        return obj.url


class MetaBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaBlock
        fields = ('id', 'query_template', 'position', 'type')


class TemplateSerializer(serializers.ModelSerializer):
    meta_blocks = MetaBlockSerializer(many=True)

    class Meta:
        model = Template
        fields = ('id', 'name', 'meta_blocks')


class CreateTemplateSerializer(serializers.ModelSerializer):
    meta_blocks = MetaBlockSerializer(many=True)

    class Meta:
        model = Template
        fields = ('theme', 'name', 'meta_blocks')

    @atomic
    def create(self, validated_data):
        name = validated_data.get('name')
        theme = validated_data.get('theme')
        meta_blocks = validated_data.get('meta_blocks')

        template = Template.objects.create(name=name, theme=theme)

        meta_blocks = [
            MetaBlock(
                query_template=block.get('query_template'),
                position=block.get('position'),
                type=block.get('type', MetaBlock.PLOTLY),
                template=template
            )
            for block in meta_blocks
        ]

        MetaBlock.objects.bulk_create(objs=meta_blocks)

        return template


class ThemeSerializer(serializers.ModelSerializer):
    templates = TemplateSerializer(many=True)

    class Meta:
        model = Theme
        fields = ('id', 'name', 'templates')


class CreateReportSerializer(serializers.ModelSerializer):
    template = serializers.IntegerField()
    search_query = serializers.CharField()

    class Meta:
        model = Report
        fields = (
            'template',
            'search_query',
            'search_start',
            'search_end'
        )

    def get_data_from_search_engine(self, search_query_text, meta_block_type, materialized_blocks):
        # TODO: выкидывать то, что уже показали пользователю
        if search_engine:
            result = search_engine.search(
                search_query_text
            )
            THRESHOLD_FOR_LOCAL_SEARCH = 30
            result = list(
                filter(lambda x: x[1] >= THRESHOLD_FOR_LOCAL_SEARCH, result))
            print(result)
            index_ids = list(map(lambda x: x[0], result))
            data = Data.objects.filter(
                id__in=index_ids
            ).all()
            if data.count() > 0:
                print(f'DATA: {data}\nmeta_block_type: {meta_block_type}')
                for item in data:
                    print(item.data_type)
                    # Грязный хак
                    # Раньше записывали в базу что-то странное (DATA_TYPES, а не конкретный тип)
                    # Сейчас понимаем, что это на самом деле плотли объект.
                    is_old_type = len(str(item.data_type)) > 15
                    item_data_type = 'plotly' if is_old_type else item.data_type
                    if meta_block_type == item_data_type:
                        return item
            else:
                return None

    def represent_data_obj(self, data_obj, block_type):
        if data_obj:
            if block_type == MetaBlock.TEXT or block_type == MetaBlock.VIDEO:
                # print(f'BLOCK TYPE: {block_type}')
                # print(data_obj.data)
                return {'text': data_obj.data}
            entity = model_to_dict(data_obj)
            entity['frame'] = entity['data']
            entity['meta'] = entity['meta_data'].get('title', '')
            entity = preprocess_entity(entity)
            print(entity['frame'])
            representation = get_one_figure_by_entity(
                entity=entity,
                return_plotly_format=True if block_type == MetaBlock.PLOTLY else False
            )
            print(representation)
            return representation.to_dict()
        return {}

    def local_search(self, search_query_text, meta_block_type, materialized_blocks):
        data_obj = self.get_data_from_search_engine(
            search_query_text, meta_block_type, materialized_blocks)
        if data_obj is not None:
            return data_obj
            # representation = self.represent_data_obj(data_obj, meta_block_type)
            # return representation

    def global_search(self, search_query_text, meta_block_type, materialized_blocks):
        # 1 - ищу в поиске урлы
        # 2 - TODO: фильтруем на то, что уже показали пользователю
        # 3 - ищу, скачивали ли мы их
        #     3.1 - скачивали, тип тот же - показываю
        #     3.2 - скачивали, тип не тот - пропускаю
        #     3.3 - не скачивали - скачиваем
        ya_ru_search_types = [MetaBlock.TEXT, MetaBlock.PLOTLY]
        video_search_types = [MetaBlock.VIDEO]
        to_index_ya_ru = []
        to_index_youtube = []
        if meta_block_type in ya_ru_search_types:
            to_index_ya_ru, data_obj = self.resolve_ya_ru_search(
                search_query_text, meta_block_type)
        elif meta_block_type in video_search_types:
            to_index_youtube, data_obj = self.resolve_video_type(
                search_query_text)
        else:
            raise ValueError(f'No meta_block type: {meta_block_type}')
        return {
            'data_obj': data_obj,
            'representation': self.represent_data_obj(data_obj, meta_block_type),
            'to_index_ya_ru': to_index_ya_ru,
            'to_index_youtube': to_index_youtube
        }

    def resolve_ya_ru_search(self, search_query, meta_block_type):
        search = ya_search(
            search_query,
            YANDEX_SEARCH_API_TOKEN
        )

        urls = [r.get('url') for r in search]
        parsed_pages = WebPage.objects.filter(url__in=urls).all()
        parsed_urls = [page.url for page in parsed_pages]
        indexed_data = Data.objects.filter(page__in=parsed_pages).all()
        to_index = set(urls).difference(set(parsed_urls))
        to_index = list(to_index)
        for data_obj in indexed_data:
            if data_obj.data_type == meta_block_type:
                return to_index, data_obj
        return to_index, None

    def resolve_text_type(self, search_query):
        search = ya_search(
            search_query,
            YANDEX_SEARCH_API_TOKEN
        )

        urls = [r.get('url') for r in search]
        parsed_pages = WebPage.objects.filter(url__in=urls).all()
        parsed_urls = [page.url for page in parsed_pages]
        indexed_data = Data.objects.filter(
            type=Data.TEXT, page__in=parsed_pages).all()

        urls_to_parse = []
        if indexed_data:
            representation = self.represent_data_obj(
                indexed_data[0], MetaBlock.TEXT)
        else:
            urls_to_parse += list(set(urls).difference(set(parsed_urls)))
            representation = {}
        return representation

    def resolve_video_type(self, search_query_text):
        video = find_youtube_video(f'{search_query_text} аналитика')
        url = video['url']
        video_page = WebPage.objects.filter(url=url).first()
        if video_page:
            data_obj = Data.objects.filter(page=video_page).first()
            print(f'В базе найдено видео: {data_obj}')
            if not data_obj:
                data_obj = None
            return [], data_obj
        else:
            return [url], None

    def represent_meta_block(self, search_query_text, meta_block, materialized_blocks):
        # 1 - идем в локальный поиск с тем же типом
        # 2 - идем в большой поиск с тем же типом
        # 3 - если не находим тот же тип, то выдаем другой тип
        # local search
        data_obj = self.local_search(
            search_query_text, meta_block.type, materialized_blocks)
        if data_obj is not None:
            return {
                'data_obj': data_obj,
                'representation': self.represent_data_obj(data_obj, meta_block.type),
                'to_index_ya_ru': [],
                'to_index_youtube': [],
            }

        # global search
        global_search_res = self.global_search(
            search_query_text, meta_block.type, materialized_blocks)
        return global_search_res

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        template = Template.objects.get(id=validated_data.get('template'))
        raw_search_query: str = validated_data.get('search_query')
        search_start: date = validated_data.get('search_start')
        search_end: date = validated_data.get('search_end')
        if search_start is not None:
            search_start = search_start.strftime('%Y%m%d')
        if search_end is not None:
            search_end = search_end.strftime('%Y%m%d')

        search_query, _ = SearchQuery.objects.get_or_create(
            user=user,
            text=raw_search_query
        )

        report = Report.objects.create(
            user=user,
            search_query=search_query,
            template=template
        )

        materialized_blocks = []

        search_by_date = ''
        if search_start is not None and search_end is None:
            search_by_date = f'date:>{search_start}'
        if search_start is None and search_end is not None:
            search_by_date = f'date:<{search_end}'
        if search_start is not None and search_end is not None:
            search_by_date = f'date:{search_start}..{search_end}'

        for meta_block in template.meta_blocks.all():
            search_query_text = f'{meta_block.query_template} {search_query} {search_by_date}'
            repr = self.represent_meta_block(
                search_query_text, meta_block, materialized_blocks)
            data_obj = repr['data_obj']
            representation = repr['representation']
            to_index_ya_ru = repr['to_index_ya_ru']
            to_index_youtube = repr['to_index_youtube']

            type = 'text' if meta_block.type == 'video' else meta_block.type

            # print(representation)
            block = ReportBlock.objects.create(
                report=report,
                data=data_obj,
                type=type,
                representation=representation,
                position=meta_block.position,
                readiness=ReportBlock.READY if data_obj else ReportBlock.NOT_READY
            )

            materialized_blocks.append(block)

            if representation == {}:
                if to_index_youtube:
                    add_video_data_to_report_block.apply_async(
                        args=(block.id, meta_block.id, to_index_youtube),
                        countdown=15
                    )
                if to_index_ya_ru:
                    add_search_data_to_report_block.apply_async(
                        args=(block.id, to_index_ya_ru),
                        countdown=15
                    )

            # if not data_obj:
            #     add_data_to_report_block.apply_async(
            #         args=(block.id, meta_block.id),
            #         countdown=15
            #     )

        return report


class UpdateReportBlockComment(serializers.ModelSerializer):
    class Meta:
        model = ReportBlock
        fields = ('comment',)


class ReportBlockSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    representation = serializers.SerializerMethodField()

    class Meta:
        model = ReportBlock
        fields = (
            'id',
            'source',
            'readiness',
            'type',
            'representation',
            'position',
            'comment',
            'summary',
        )

    def get_source(self, obj):
        return obj.source

    def get_summary(self, obj):
        return markdown.markdown(obj.summary)

    def get_representation(self, obj):
        if 'text' in obj.representation:
            return markdown.markdown(obj.representation['text'])
        return obj.representation


class ReportBlockSummaryModelSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=(
            ('yandexgpt', 'yandexgpt'),
            ('yandexgpt-lite', 'yandexgpt-lite')
        )
    )

    class Meta:
        model = ReportBlock
        fields = ('type',)


class ReportLightSerializer(serializers.ModelSerializer):
    search_query = serializers.StringRelatedField()
    theme = serializers.SerializerMethodField()
    template = serializers.StringRelatedField()
    readiness = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'theme', 'template',
            'search_query',
            'date', 'readiness'
        )

    def get_theme(self, obj):
        return str(obj.theme)

    def get_readiness(self, obj):
        # В проде надо такое оптимизировать
        return not obj.blocks.filter(readiness=ReportBlock.NOT_READY).exists()


class ReportSerializer(ReportLightSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'theme', 'template',
            'search_query',
            'blocks', 'date',
            'readiness', 'search_start',
            'search_end'
        )

    def get_blocks(self, obj):
        return ReportBlockSerializer(
            obj.blocks.all().annotate(
                source=models.F('data__page__url')
            ),
            many=True
        ).data


class ReportFileFormatSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=(
            ('pdf', 'pdf'),
            ('msword', 'word'),
            ('vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'excel')
        )
    )

    class Meta:
        model = Report
        fields = ('type',)


# ============================================================================
# TITAN Analytics Platform - Extended Serializers
# ============================================================================

from accounts.models import TemplateCategory, DataSource, UserPreferences


class TemplateCategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий шаблонов"""
    subcategories = serializers.SerializerMethodField()
    templates_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TemplateCategory
        fields = (
            'id', 'name', 'slug', 'icon', 
            'description', 'parent', 'position',
            'subcategories', 'templates_count'
        )
    
    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return TemplateCategorySerializer(
                obj.subcategories.all(), 
                many=True
            ).data
        return []
    
    def get_templates_count(self, obj):
        return obj.templates.count()


class TemplateMarketplaceSerializer(serializers.ModelSerializer):
    """Сериализатор для публичного Marketplace"""
    theme_name = serializers.CharField(source='theme.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    blocks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Template
        fields = (
            'id', 'name', 'description', 
            'theme_name', 'category_name', 'category_slug',
            'tags', 'use_count', 'rating', 
            'is_premium', 'author_name',
            'blocks_count', 'created_at'
        )
    
    def get_blocks_count(self, obj):
        return obj.meta_blocks.count()


class MetaBlockDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор мета-блока"""
    data_sources_names = serializers.SerializerMethodField()
    
    class Meta:
        model = MetaBlock
        fields = (
            'id', 'query_template', 'type', 'position',
            'filters', 'processing_params', 
            'data_sources', 'data_sources_names'
        )
    
    def get_data_sources_names(self, obj):
        return [ds.name for ds in obj.data_sources.all()]


class TemplateDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор шаблона с мета-блоками"""
    meta_blocks = MetaBlockDetailSerializer(many=True, read_only=True)
    theme_name = serializers.CharField(source='theme.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Template
        fields = (
            'id', 'name', 'description', 
            'theme', 'theme_name',
            'category', 'category_name',
            'tags', 'is_public', 'is_premium',
            'use_count', 'rating',
            'meta_blocks', 'created_at'
        )


class TemplateExportSerializer(serializers.Serializer):
    """Сериализатор для экспорта шаблона"""
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    theme = serializers.CharField(required=False, allow_null=True)
    category = serializers.CharField(required=False, allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    meta_blocks = serializers.ListField(required=False)
    version = serializers.CharField(default='1.0')
    exported_by = serializers.CharField(default='TITAN Analytics Platform')


class TemplateImportSerializer(serializers.Serializer):
    """Сериализатор для импорта шаблона"""
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    theme = serializers.CharField(required=False, allow_null=True)
    category = serializers.CharField(required=False, allow_null=True)
    tags = serializers.ListField(
        child=serializers.CharField(), 
        required=False, 
        default=list
    )
    meta_blocks = serializers.ListField(required=True)
    
    def validate_meta_blocks(self, value):
        """Валидация структуры мета-блоков"""
        for block in value:
            required_fields = ['query_template', 'type', 'position']
            for field in required_fields:
                if field not in block:
                    raise serializers.ValidationError(
                        f'Поле {field} обязательно для каждого мета-блока'
                    )
            
            # Проверка типа блока
            valid_types = [choice[0] for choice in MetaBlock.TYPES]
            if block['type'] not in valid_types:
                raise serializers.ValidationError(
                    f'Недопустимый тип блока: {block["type"]}'
                )
        
        return value


class DataSourceSerializer(serializers.ModelSerializer):
    """Сериализатор источников данных"""
    
    class Meta:
        model = DataSource
        fields = (
            'id', 'name', 'source_type', 
            'base_url', 'api_key_required', 
            'is_active', 'config'
        )


class UserPreferencesSerializer(serializers.ModelSerializer):
    """Сериализатор пользовательских настроек"""
    favorite_templates_details = TemplateMarketplaceSerializer(
        source='favorite_templates', 
        many=True, 
        read_only=True
    )
    
    class Meta:
        model = UserPreferences
        fields = (
            'id', 'user', 
            'favorite_templates', 'favorite_templates_details',
            'default_theme', 'default_ai_model', 
            'settings'
        )
        read_only_fields = ('user',)
