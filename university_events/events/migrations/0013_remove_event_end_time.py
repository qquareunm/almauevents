# Generated by Django 5.2.1 on 2025-05-27 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_event_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
    ]
