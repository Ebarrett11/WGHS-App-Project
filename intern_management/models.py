from django.db import models
from django.contrib.auth.models import User


class InternshipLocationModel(models.Model):
    """
        Description:
            Model describing a valid internship location

    """
    address = models.CharField(max_length=400)
    title = models.CharField(max_length=100)
    managers = models.ManyToManyField(User, related_name="+")
    students = models.ManyToManyField(User)
    description = models.TextField()
    contact_email = models.EmailField(default="")
    # colon deliminated list of hashed valid tokens (Not to be shown to users)
    outstanding_tokens = models.TextField(null=True)
    # comma deliminated list of tags that apply to this location
    tags = models.TextField(null=True)

    def __str__(self):
        return self.title


class LoggedHoursModel(models.Model):
    """
        Description:
            Model describing logged hours for a certain location

    """
    total_hours = models.IntegerField(default=0)
    location = models.ForeignKey(InternshipLocationModel,
                                 on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)
    id = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return "Logged Hours for " + self.user.username
