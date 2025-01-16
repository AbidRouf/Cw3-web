from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class Hobby(models.Model):
    """Represents a hobby for users to associate with on the platform"""
    name: str = models.CharField(max_length=100)

    def __str__(self) -> str:
        """
        Returns the hobby into its corresponding string representation
        """
        return self.name

class User(AbstractUser):
    """
    this will extend the default user model to include date of birth and hobbies and to grant the user the ability to have friends on the platform
    """
    dob: models.DateField = models.DateField(
        verbose_name="Date of Birth"
    )
    hobbies: models.ManyToManyField = models.ManyToManyField(Hobby)
    friends: models.ManyToManyField = models.ManyToManyField('self', symmetrical=True, blank=True)

class FriendRequest(models.Model):
    from_user: User = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user: User = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    accepted: bool = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'From {self.from_user} to {self.to_user}'

class PageView(models.Model):
    """
    This is for keeping track of the number of page views
    """
    count: int = models.IntegerField(default=0)

    def __str__(self) -> str:
        """
        For returning the page view function count as a string
        """
        return f"Page view count: {self.count}"