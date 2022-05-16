from distutils.command.upload import upload
import uu
from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid

AGE_CHOICES=(
    ('All','All'),
    ('Kids','Kids'),
)

MOVIE_CHOICES=(
  ('seasonal','seasonal'),
  ('single','single')  
)

class CustomUser(AbstractUser):
    profiles=models.ManyToManyField('Profile',null=True, blank=True)

class Profile(models.Model):
    name=models.CharField(max_length=255)
    age_limit=models.CharField(max_length=10, choices=AGE_CHOICES)
    uuid=models.UUIDField(default=uuid.uuid4)
    
class Movie(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField(blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    uuid=models.UUIDField(default=uuid.uuid4)
    type=models.CharField(max_length=10, choices=MOVIE_CHOICES)
    videos=models.ManyToManyField('Video')
    flyer=models.ImageField(upload_to='flyers')
    age_limit=models.CharField(max_length=10, choices=AGE_CHOICES)

class Video(models.Model0):
    title=models.CharField(max_length=255, blank=True, null=True)
    file=models.FileField(upload_to='movies')

