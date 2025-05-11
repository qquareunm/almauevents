from modeltranslation.translator import register, TranslationOptions
from .models import Event, EventType, SubCategory

@register(EventType)
class EventTypeTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'location')
