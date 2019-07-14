from django.db import models

# Create your models here.


class InternshipLocationModel(models.Model):
    address = models.CharField(max_length=400)
