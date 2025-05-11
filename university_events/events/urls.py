from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("calendar/", views.calendar_view, name="calendar"),  # Используем calendar_view
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("success/", views.success, name="success"),
    path("export-registrations/", views.export_registrations_to_excel, name="export_registrations"),
    path("settings/", views.admin_settings, name="admin_settings"),  # Измененный маршрут
    path("export/", views.export_registrations_to_excel, name="export_registrations"),
]