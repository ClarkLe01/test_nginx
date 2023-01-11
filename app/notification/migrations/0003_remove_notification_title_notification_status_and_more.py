# Generated by Django 4.1.4 on 2023-01-11 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0002_testnotify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='title',
        ),
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
