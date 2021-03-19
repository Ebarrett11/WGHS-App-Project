# Generated by Django 2.2.4 on 2019-08-24 07:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern_management', '0034_auto_20190823_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internshiplocationmodel',
            name='outstanding_tokens',
        ),
        migrations.AlterField(
            model_name='availableworkmodel',
            name='students',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]