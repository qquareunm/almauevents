# Generated by Django 5.2.1 on 2025-05-27 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_event_end_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
    ]
