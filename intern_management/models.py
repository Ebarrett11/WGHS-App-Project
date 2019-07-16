from django.db import models

# Create your models here.


class InternshipLocationModel(models.Model):
    address = models.CharField(max_length=400)
    title = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.title
