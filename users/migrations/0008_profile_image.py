# Generated by Django 2.2.4 on 2019-08-22 00:17

from django.db import migrations, models
import intern_management.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to='', validators=[intern_management.validators.validate_image_size]),
        ),
    ]
