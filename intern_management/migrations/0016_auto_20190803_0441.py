# Generated by Django 2.1.10 on 2019-08-03 04:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intern_management', '0015_auto_20190803_0440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internshiplocationmodel',
            name='manager',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]