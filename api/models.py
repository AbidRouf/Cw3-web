from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Hobby(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    dob = models.DateField(
        verbose_name="Date of Birth"
    )
    hobbies = models.ManyToManyField(Hobby)


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
