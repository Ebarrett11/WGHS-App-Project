# Generated by Django 2.1.10 on 2019-08-04 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intern_management', '0018_auto_20190804_0432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='internshiplocationmodel',
            old_name='outstanding_token',
            new_name='outstanding_tokens',
        ),
    ]
