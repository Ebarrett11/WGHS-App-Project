from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    choices = [
        ('Student', 'Student'),
        ('Man', 'Location Manager'),
    ]
    type = models.CharField(choices=choices, max_length=7)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
