from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    publisher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posted_by")
    tweet = models.CharField(max_length=280)
    date_time = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "publisher": self.publisher.username,
            "tweet": self.tweet,
            "date_time": self.date_time.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }

    def __str__(self):
        return f"{self.tweet} by {self.publisher}"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    date_followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} has followed {self.followee}"
