# Generated by Django 5.0.1 on 2024-02-28 16:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0005_attendance'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to=settings.AUTH_USER_MODEL),
        ),
    ]
