# Generated by Django 5.0.1 on 2024-03-09 11:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0010_alter_complaint_uploaded_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdetails',
            name='roomNo',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomNo', models.IntegerField()),
                ('floorNo', models.IntegerField()),
                ('Availability', models.BooleanField(default=True)),
                ('NoOfOccupents', models.IntegerField(default=0)),
                ('occupants', models.ManyToManyField(blank=True, related_name='rooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
