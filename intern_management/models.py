from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class InternshipLocationModel(models.Model):
    address = models.CharField(max_length=400)
    title = models.CharField(max_length=100)
    manager = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, related_name="+")
    students = models.ManyToManyField(User)
    description = models.TextField()
    contact_email = models.EmailField(default="")

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ('can_confirm', 'User can confirm hours for this location')
        ]
