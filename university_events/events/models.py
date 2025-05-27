from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class EventType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default="#007bff")

    def get_text_color(self):
        """Определяем, какой цвет текста будет лучше читаться"""
        hex_color = self.color.lstrip("#")
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return "#ffffff" if brightness < 128 else "#000000"

    def styled_name(self):
        """Возвращаем HTML с цветной кнопкой"""
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 5px 10px; border-radius: 5px;">{}</span>',
            self.color, self.get_text_color(), _(self.name)  # Используем перевод
        )

    def __str__(self):
        return (self.name)  # Переводим строку на уровне модели


class SubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="subcategories")  # Связь с типом события

    def __str__(self):
        return (self.name)  # Переводим строку на уровне модели

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="event_images/", null=True, blank=True)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    report = models.TextField(blank=True, null=True, help_text="Отчёт о том, как прошло мероприятие")

    def __str__(self):
        return self.title


class Registration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        unique_together = ('email', 'event')  

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event.title}"


class MainImage(models.Model):
    image = models.ImageField(upload_to="event_images/", null=True, blank=True)


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='event_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"Image for {self.event.title}"

