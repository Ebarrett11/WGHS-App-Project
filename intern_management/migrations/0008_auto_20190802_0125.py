# Generated by Django 2.1.10 on 2019-08-02 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intern_management', '0007_remove_internshiplocationmodel_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='internshiplocationmodel',
            options={'permissions': [('confirm_hours', 'Can Person Confirm Hours')]},
        ),
    ]
