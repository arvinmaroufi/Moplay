from django.urls import path
from . import views


app_name = 'movie'

urlpatterns = [
    path('movies/', views.movies_list, name='movies'),
]
