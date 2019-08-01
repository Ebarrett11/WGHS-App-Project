from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class InternshipLocationModel(models.Model):
    address = models.CharField(max_length=400)
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ManyToManyField(User)
    contact_email = models.EmailField(default="")

    def __str__(self):
        return self.title
