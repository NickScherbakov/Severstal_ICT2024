"""
TITAN Analytics Platform - Extended API Views
Новые endpoints для marketplace, категорий, источников данных и т.д.
"""

from rest_framework import decorators, viewsets, status, mixins, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db import models
from drf_spectacular import utils as spectacular_utils

from accounts.models import (
    Template, TemplateCategory, DataSource, 
    UserPreferences, MetaBlock
)
from accounts.processors import ProcessorRegistry
from . import serializers


class TemplateCategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для категорий шаблонов
    """
    queryset = TemplateCategory.objects.all()
    serializer_class = serializers.TemplateCategorySerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Только родительские категории (без parent)
        parent_only = self.request.query_params.get('parent_only', None)
        if parent_only:
            queryset = queryset.filter(parent__isnull=True)
        return queryset


class TemplateMarketplaceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Публичный Marketplace шаблонов
    """
    queryset = Template.objects.filter(is_public=True).select_related('theme', 'category')
    serializer_class = serializers.TemplateMarketplaceSerializer
    permission_classes = (AllowAny,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['use_count', 'rating', 'created_at']
    ordering = ['-use_count', '-rating']
    
    @spectacular_utils.extend_schema(
        parameters=[
            spectacular_utils.OpenApiParameter(
                name='category', 
                description='Slug категории для фильтрации', 
                type=str
            ),
            spectacular_utils.OpenApiParameter(
                name='premium', 
                description='Только премиум шаблоны', 
                type=bool
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Фильтр по категории
        category_slug = request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Фильтр премиум
        premium = request.query_params.get('premium', None)
        if premium is not None:
            is_premium = premium.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(is_premium=is_premium)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TemplateExtendedViewSet(viewsets.ModelViewSet):
    """
    Расширенный ViewSet для работы с шаблонами
    Включает экспорт/импорт, избранное
    """
    queryset = Template.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.action == 'export_template':
            return serializers.TemplateExportSerializer
        if self.action == 'import_template':
            return serializers.TemplateImportSerializer
        return serializers.TemplateDetailSerializer
    
    @decorators.action(
        methods=['post'], 
        detail=True,
        url_name='export'
    )
    def export_template(self, request, pk=None):
        """
        Экспорт шаблона в JSON для обмена
        """
        template = self.get_object()
        
        # Увеличиваем счетчик использования
        template.use_count += 1
        template.save(update_fields=['use_count'])
        
        data = {
            'name': template.name,
            'description': template.description,
            'theme': template.theme.name if template.theme else None,
            'category': template.category.slug if template.category else None,
            'tags': template.tags,
            'meta_blocks': [
                {
                    'query_template': block.query_template,
                    'type': block.type,
                    'position': block.position,
                    'filters': block.filters,
                    'processing_params': block.processing_params,
                }
                for block in template.meta_blocks.all().order_by('position')
            ],
            'version': '1.0',
            'exported_by': 'TITAN Analytics Platform'
        }
        
        serializer = serializers.TemplateExportSerializer(data)
        return Response(serializer.data)
    
    @decorators.action(
        methods=['post'], 
        detail=False,
        url_name='import'
    )
    def import_template(self, request):
        """
        Импорт шаблона из JSON
        """
        from accounts.models import Theme, TemplateCategory, MetaBlock
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Получаем или создаём тему
        theme = None
        if data.get('theme'):
            theme, _ = Theme.objects.get_or_create(name=data['theme'])
        
        # Получаем категорию
        category = None
        if data.get('category'):
            try:
                category = TemplateCategory.objects.get(slug=data['category'])
            except TemplateCategory.DoesNotExist:
                pass
        
        # Создаём шаблон
        template = Template.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            theme=theme,
            category=category,
            tags=data.get('tags', []),
            author=request.user,
            is_public=False  # По умолчанию приватный
        )
        
        # Создаём мета-блоки
        for block_data in data.get('meta_blocks', []):
            MetaBlock.objects.create(
                query_template=block_data['query_template'],
                template=template,
                type=block_data['type'],
                position=block_data['position'],
                filters=block_data.get('filters', {}),
                processing_params=block_data.get('processing_params', {})
            )
        
        result_serializer = serializers.TemplateDetailSerializer(template)
        return Response(
            result_serializer.data, 
            status=status.HTTP_201_CREATED
        )
    
    @decorators.action(
        methods=['post'], 
        detail=True,
        url_name='favorite'
    )
    def toggle_favorite(self, request, pk=None):
        """
        Добавить/удалить шаблон из избранного
        """
        template = self.get_object()
        preferences, _ = UserPreferences.objects.get_or_create(user=request.user)
        
        if template in preferences.favorite_templates.all():
            preferences.favorite_templates.remove(template)
            is_favorite = False
        else:
            preferences.favorite_templates.add(template)
            is_favorite = True
        
        return Response({
            'is_favorite': is_favorite,
            'message': 'Добавлено в избранное' if is_favorite else 'Удалено из избранного'
        })
    
    @decorators.action(
        methods=['get'], 
        detail=False,
        url_name='my-templates'
    )
    def my_templates(self, request):
        """
        Шаблоны текущего пользователя
        """
        queryset = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @decorators.action(
        methods=['get'], 
        detail=False,
        url_name='favorites'
    )
    def favorites(self, request):
        """
        Избранные шаблоны пользователя
        """
        try:
            preferences = request.user.preferences
            queryset = preferences.favorite_templates.all()
        except UserPreferences.DoesNotExist:
            queryset = Template.objects.none()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DataSourceViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для источников данных
    """
    queryset = DataSource.objects.filter(is_active=True)
    serializer_class = serializers.DataSourceSerializer
    permission_classes = (IsAuthenticated,)
    
    @spectacular_utils.extend_schema(
        parameters=[
            spectacular_utils.OpenApiParameter(
                name='type', 
                description='Фильтр по типу источника', 
                type=str
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        source_type = request.query_params.get('type', None)
        if source_type:
            queryset = queryset.filter(source_type=source_type)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserPreferencesViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для пользовательских настроек
    """
    serializer_class = serializers.UserPreferencesSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        """
        Возвращает preferences текущего пользователя
        """
        preferences, _ = UserPreferences.objects.get_or_create(user=self.request.user)
        return preferences
    
    @decorators.action(
        methods=['get'], 
        detail=False,
        url_name='me'
    )
    def me(self, request):
        """
        Получить настройки текущего пользователя
        """
        preferences = self.get_object()
        serializer = self.get_serializer(preferences)
        return Response(serializer.data)


class ProcessorInfoViewSet(viewsets.ViewSet):
    """
    Информация о зарегистрированных обработчиках данных
    """
    permission_classes = (IsAuthenticated,)
    
    @decorators.action(
        methods=['get'], 
        detail=False,
        url_name='list-processors'
    )
    def list_processors(self, request):
        """
        Список всех зарегистрированных процессоров
        """
        processors = ProcessorRegistry.list_processors()
        return Response({
            'count': len(processors),
            'processors': processors
        })
    
    @decorators.action(
        methods=['get'], 
        detail=False,
        url_name='block-types'
    )
    def block_types(self, request):
        """
        Доступные типы блоков
        """
        return Response({
            'types': [
                {'value': choice[0], 'label': choice[1]} 
                for choice in MetaBlock.TYPES
            ]
        })
