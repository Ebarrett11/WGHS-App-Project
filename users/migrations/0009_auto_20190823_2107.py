# Generated by Django 2.2.4 on 2019-08-24 02:07

from django.db import migrations, models
import intern_management.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to='user_profile_pics', validators=[intern_management.validators.validate_image_size]),
        ),
    ]
