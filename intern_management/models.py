from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from .validators import validate_image_size


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
    outstanding_tokens = models.TextField(null=True, blank=True)
    # comma deliminated list of tags that apply to this location
    tags = models.TextField(null=True)
    image = models.ImageField(
        null=True, validators=[validate_image_size],
        upload_to="location_pictures"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'intern_management:location_details',
            kwargs={
                "pk": self.pk
            }
        )

    def get_total_hours(self, user):
        total_hours = 0
        for hours in user.loggedhoursmodel_set.all():
            if hours.location == self and hours.is_valid:
                total_hours += hours.total_hours
        return total_hours


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


# command: python manage.py makemigrations; python manage.py migrate
# add models to database
class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    location = models.ForeignKey(
        InternshipLocationModel,
        on_delete=models.CASCADE
    )
    date_posted = models.DateTimeField()

    def __str__(self):
        return "Comment by {user}".format(user=self.user.username)


class AvailableWorkModel(models.Model):
    location = models.ForeignKey(
        InternshipLocationModel,
        on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=200)
    text = models.TextField()
    contact_email = models.CharField(max_length=30)
