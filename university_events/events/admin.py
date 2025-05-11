from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Event, EventType, SubCategory, Registration, MainImage


@admin.register(EventType)
class EventTypeAdmin(TranslationAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'event_type')
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(TranslationAdmin):
    list_display = ('title', 'event_type', 'subcategory', 'date', 'location')
    list_filter = ('event_type', 'subcategory')
    search_fields = ('title', 'description')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'event')  # Поля, отображаемые в списке
    list_filter = ('event',)  # Фильтр по событию
    search_fields = ('first_name', 'last_name', 'email')  # Поиск по имени, фамилии и email

admin.site.register(MainImage)