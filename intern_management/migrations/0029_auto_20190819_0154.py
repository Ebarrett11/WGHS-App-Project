# Generated by Django 2.1.11 on 2019-08-19 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intern_management', '0028_commentmodel_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intern_management.InternshipLocationModel'),
        ),
    ]
