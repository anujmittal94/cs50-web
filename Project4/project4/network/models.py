from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postsbyuser")
    post = models.TextField(max_length = 500)
    timestamp = models.DateTimeField(auto_now_add=True, blank = True)
    likes = models.ManyToManyField(User, related_name="likesonpost", blank = True)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followsbyuser")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followsonuser")
