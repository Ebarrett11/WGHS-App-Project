from django.db import models

# Create your models here.
class InternshipLocationModel(models.Model):
    pass

class StudentModel(models.Model):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)

    def full_name(self):
        return "{} {}".format(self.fname, self.lname)

    def __str__(self):
        return self.full_name()
