from django.urls import path
from . import views


app_name = 'movie'

urlpatterns = [
    path('movies/', views.movies_list, name='movies'),
    path('series/', views.series_list, name='series'),
    path('movies/<slug:slug>/', views.movie_detail, name='movie_detail'),
]
