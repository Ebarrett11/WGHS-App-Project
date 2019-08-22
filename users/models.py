from django.db import models
from django.contrib.auth.models import User
from intern_management.validators import validate_image_size
# Create your models here.


class Profile(models.Model):
    choices = [
        ('Student', 'Student'),
        ('Man', 'Location Manager'),
    ]
    type = models.CharField(choices=choices, max_length=7)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True, validators=[validate_image_size],
        upload_to="user_profile_pics"
    )
