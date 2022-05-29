from django.contrib import admin
from .models import Movie, Profile, CustomUser, Video, WatchaMovie, WatchaRating, WatchaUser

# Register your models here.
admin.site.register(Movie)
admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(Video)
admin.site.register(WatchaMovie)
admin.site.register(WatchaUser)
admin.site.register(WatchaRating)