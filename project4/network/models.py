from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    publisher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posted_by")
    tweet = models.CharField(max_length=280)

    def __str__(self):
        return f"{self.tweet} by {self.publisher}"
