# Generated by Django 5.0.1 on 2024-02-03 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('branch', models.CharField(choices=[('CSE', 'Computer Engineering'), ('IT', 'Information Technology'), ('EnTC', 'EnTC'), ('CE', 'Civil Engineering'), ('ME', 'Mechanical Engineering')], max_length=50)),
                ('year', models.CharField(choices=[('FE', 'FE'), ('SE', 'SE'), ('TE', 'TE'), ('BE', 'BE')], max_length=2)),
                ('college', models.CharField(choices=[('TAE', 'Trinity Academy of Engineering'), ('TCOER', 'Trinity College of Engineering and Research'), ('KJCOER', 'KJ College of Engineering and Research')], max_length=50)),
                ('student_mobile', models.CharField(max_length=10)),
                ('parent_mobile', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('non', 'Non Binary'), ('na', 'Prefer Not To Say')], max_length=10)),
                ('parent_name', models.CharField(max_length=100)),
            ],
        ),
    ]
