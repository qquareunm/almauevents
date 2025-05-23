from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("calendar/", views.calendar_view, name="calendar"), 
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path('my-events/', views.my_events, name='my_events'),
    path("success/", views.success, name="success"),
    path("export-registrations/", views.export_registrations_to_excel, name="export_registrations"),
    path("settings/", views.admin_settings, name="admin_settings"),  
    path("export/", views.export_registrations_to_excel, name="export_registrations"),
]