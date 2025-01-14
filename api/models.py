from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Hobby(models.Model):
    """Represents a hobby for users to associate with on the platform"""
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns the hobby into its corresponding string representation
        """
        return self.name

class User(AbstractUser):
    """
    this will extend the default user model to include date of birth and hobbies
    """
    dob = models.DateField(
        verbose_name="Date of Birth", null=True, blank=True
    )
    hobbies = models.ManyToManyField(Hobby)


class PageView(models.Model):
    """
    This is for keeping track of the number of page views
    """
    count = models.IntegerField(default=0)

    def __str__(self):
        """
        For returning the page view function count as a string
        """
        return f"Page view count: {self.count}"

class friendRequests(models.Model):
    """this is for sending and recieving friend requests"""
    receiving = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")
    sending = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    requeststatus = models.CharField(
        max_length=10,
        choices=[('pendingrq', 'Pendingrq'), ('acceptedrq', 'Acceptedrq')],
        default='pendingrq'
    )
    rqsentat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"
    
