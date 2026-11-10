from django.db import models
from django.contrib.auth import login, logout
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=100)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    is_archive = models.BooleanField(default=True)

    def __str__(self):
        return self.username



class Post(models.Model):
    class PostType(models.TextChoices):
        PHOTO = 'photo', 'Photo'
        VIDEO = 'video', 'Video'
        PHOTO_VIDEO = 'photo_video', 'Photo + video'
        REELS = 'reels', 'Reels'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=20, choices=PostType.choices, default=PostType.PHOTO)
    about = models.CharField(max_length=3000)
    location = models.CharField(max_length=100, blank=True, null=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.id}"


class PostMedia(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    file = models.FileField(upload_to='posts/')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.file.name
