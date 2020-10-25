# Generated by Django 3.1.2 on 2020-10-21 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0009_auto_20201020_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('issue', models.CharField(choices=[('Report a bug', 'Report a bug'), ('Feature Request', 'Feature Request'), ('Enhancement', 'Enhancement')], default='Report a bug', max_length=100)),
                ('message', models.TextField()),
                ('name', models.ForeignKey(default=15, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]