# Generated by Django 2.2.4 on 2019-08-21 23:37

from django.db import migrations, models
import intern_management.validators


class Migration(migrations.Migration):

    dependencies = [
        ('intern_management', '0031_availableworkmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='internshiplocationmodel',
            name='image',
            field=models.ImageField(null=True, upload_to='', validators=[intern_management.validators.validate_image_size]),
        ),
    ]
