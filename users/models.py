from django.db import models
from intern_management.models import InternshipLocationModel
from django.contrib.auth.models import User
# Create your models here.


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    locations = models.ManyToManyField(InternshipLocationModel)

    def __str__(self):
        return "Profile of " + self.user.username
