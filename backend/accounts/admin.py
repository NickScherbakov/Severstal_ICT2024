from django.contrib import admin

from . import models


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Template)
class TemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MetaBlock)
class MetaBlockAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Data)
class DataAdmin(admin.ModelAdmin):
    readonly_fields = ('page', 'file')


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ReportBlock)
class ReportBlockAdmin(admin.ModelAdmin):
    pass


@admin.register(models.WebPage)
class WebPageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Files)
class FilesAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_type', 'is_active', 'api_key_required')
    list_filter = ('source_type', 'is_active', 'api_key_required')
    search_fields = ('name', 'base_url')


@admin.register(models.TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'position')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_ai_model', 'default_theme')
    list_filter = ('default_ai_model',)
    search_fields = ('user__username',)
