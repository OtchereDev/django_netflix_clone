from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from sqlalchemy import true

# choices field (DB에 저장할 실제 값, display용 이름)
AGE_CHOICES=(
    ('All','All'),
    ('Kids','Kids')
)

MOVIE_CHOICE=(
    ('seasonal','Seasonal'),
    ('single','Single')
)

# Create your models here.
class CustomUser(AbstractUser): # User Model을 커스텀하여 테이블에 열을 추가 (https://wikidocs.net/6651)
    profiles = models.ManyToManyField('Profile',blank=True) # 다대다 관계, Profile테이블을 참조 (https://velog.io/@jiffydev/Django-9.-ManyToManyField-1)

class Profile(models.Model):
    name=models.CharField(max_length=225)
    age_limit=models.CharField(max_length=10,choices=AGE_CHOICES)
    uuid=models.UUIDField(default=uuid.uuid4) # UUID(universally unique identifier) '범용 고유 식별자'를 저장하는 데이터타입 (https://ko.wikipedia.org/wiki/범용_고유_식별자)

    def __str__(self):
        return self.name +" "+self.age_limit

class Movie(models.Model):
    title=models.CharField(max_length=225)
    description=models.TextField(blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    uuid=models.UUIDField(default=uuid.uuid4)
    type=models.CharField(max_length=10,choices=MOVIE_CHOICE)
    videos=models.ManyToManyField('Video')
    flyer=models.ImageField(upload_to='flyers')
    age_limit=models.CharField(max_length=10,choices=AGE_CHOICES)

class Video(models.Model):
    title=models.CharField(max_length=225,blank=True,null=True)
    file=models.FileField(upload_to='movies')

#============================================================
"""             왓챠피디아 DB         """
class WatchaMovie(models.Model):
    movie_index=models.IntegerField()
    movie_id=models.CharField(max_length=225)
    movie_name=models.CharField(max_length=225)
    movie_url=models.CharField(max_length=225)


class WatchaUser(models.Model):
    user_index=models.IntegerField()
    user_id=models.CharField(max_length=225)
    user_name=models.CharField(max_length=64)
    user_url=models.CharField(max_length=225)
    user_email=models.CharField(max_length=225)


class WatchaRating(models.Model):
    user_index=models.IntegerField()
    movie_index=models.IntegerField()
    rating=models.FloatField()


