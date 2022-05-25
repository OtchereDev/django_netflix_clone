from django.urls import path

from core.models import Movie
from .views import Home, ProfileList, ProfileCreate, Watch, ShowMovieDetail, ShowMovie

app_name = 'core'

 # 클래스형 뷰(as_view()) (https://coshin.tistory.com/13)
urlpatterns = [
    path('',Home.as_view()),
    path('profile/',ProfileList.as_view(),name='profile_list'),
    path('profile/create/',ProfileCreate.as_view(),name='profile_create'),
    path('watch/<str:profile_id>/',Watch.as_view(),name='watch'),
    path('movie/detail/<str:movie_id>/',ShowMovieDetail.as_view(),name='show_det'),
    path('movie/play/<str:movie_id>',ShowMovie.as_view(),name='play'),
]
