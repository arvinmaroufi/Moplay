from django.urls import path
from . import views


app_name = 'movie'

urlpatterns = [
    path('movies/', views.movies_list, name='movies'),
    path('series/', views.series_list, name='series'),
    path('movies/<slug:slug>/', views.movie_detail, name='movie_detail'),
    path('series/<slug:slug>/', views.series_detail, name='series_detail'),
    path('movies/watch/<slug:slug>/', views.movie_watch, name='movie_watch'),
    path('series/watch/<slug:series_slug>/<int:video_id>/', views.series_watch, name='series_watch'),
    path('series/download/<slug:series_slug>/<str:quality>/', views.series_download, name='series_download'),
    path('genre/movies/<slug:slug>/', views.genre_movies, name='genre_movies'),
]
