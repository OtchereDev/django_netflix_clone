from ast import Try
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import profileForm
from .models import Movie, Profile, WatchaMovie, WatchaUser, WatchaRating
import pandas as pd

# Create your views here.

class Watcha(View):
    def get(self,request,*args, **kwargs): 
        watchauser=WatchaUser.objects.get(user_index=416)
        watcharating=WatchaRating.objects.filter(user_index=416)

        movie_name_list = []
        movie_url_list = []
        movie_list = []
        for item in watcharating:
            selected_movie = WatchaMovie.objects.get(movie_index=item.movie_index)
            movie_name_list.append(selected_movie.movie_name)
            movie_url_list.append(selected_movie.movie_url)
            movie_list.append(selected_movie)

        selected_movie_df = pd.DataFrame({'movie_names':movie_name_list,'movie_urls':movie_url_list})

        watcharating=watcharating.values()
        context = {'watchauser':watchauser, 'watcharating':watcharating, 'movie_name_list':movie_name_list, 'selected_movie_df':selected_movie_df.loc[:3].to_html(justify='center'), 
        'movie_list':movie_list}

        return render(request,'watchamovie.html',context)



class Home(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('core:profile_list')
        return render(request,'index.html')


# 복잡한 코드가 여러 함수에 중복적으로 들어가야할 경우 decorator 를 통해서 단순화 해 줄 수 있습니다.
@method_decorator(login_required,name='dispatch') # https://ssungkang.tistory.com/entry/Django-FBV-와-CBV-의-decorators-사용법
class ProfileList(View):
    def get(self,request,*args,**kwargs):
        profiles=request.user.profiles.all()
        return render(request,'profileList.html',{
            'profiles':profiles
        })



@method_decorator(login_required,name='dispatch')
class ProfileCreate(View):
    def get(self,request,*args, **kwargs):
        # form for creating profile
        form=profileForm()

        return render(request,'profileCreate.html',{
            'form':form
        })

    def post(self,request,*args, **kwargs):
        form=profileForm(request.POST or None)

        if form.is_valid():
            # print(form.cleaned_data)
            profile = Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect('core:profile_list')
        
        return render(request,'profileCreate.html',{
            'form':form
        })


@method_decorator(login_required,name='dispatch')
class Watch(View):
    def get(self,request,profile_id,*args, **kwargs):
        try:
            profile=Profile.objects.get(uuid=profile_id)
            movies=Movie.objects.filter(age_limit=profile.age_limit)
            watchamovie=WatchaMovie.objects.all()    
            context = {'movies':movies, 'watchamovie': watchamovie}

            if profile not in request.user.profiles.all():
                return redirect(to='core:profile_list')
            
            return render(request,'movieList.html',context)
        except Profile.DoesNotExist:
            return redirect(to='core:profile_list')


@method_decorator(login_required,name='dispatch')
class ShowMovieDetail(View):
    def get(self,request,movie_id,*args, **kwargs):
        try:
            movie=Movie.objects.get(uuid=movie_id)

            return render(request,'movieDetail.html',{
                'movie':movie
            })
        except Movie.DoesNotExist:
            return redirect('core:profile_list')


@method_decorator(login_required,name='dispatch')
class ShowMovie(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie=Movie.objects.get(uuid=movie_id)
            movie=movie.videos.values()

            return render(request,'showMovie.html',{
                'movie':list(movie)
            })

        except Movie.DoesNotExist:
            return redirect('core:profile_list')


#=====================================================================