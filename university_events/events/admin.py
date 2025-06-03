from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Event, EventType, SubCategory, Registration, MainImage, EventImage


@admin.register(EventType)
class EventTypeAdmin(TranslationAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'event_type')
    search_fields = ('name',)


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


@admin.register(Event)
class EventAdmin(TranslationAdmin):  
    list_display = ('title', 'date')
    fields = ('title', 'description', 'date', 'start_time', 'location', 'image', 'event_type', 'subcategory', 'report')
    search_fields = ('title', 'description')
    inlines = [EventImageInline]


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'event', 'created_at')
    list_filter = ('event', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'event__title')


admin.site.register(MainImage)

