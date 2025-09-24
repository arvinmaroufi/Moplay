from django.shortcuts import render
from movie.models import Movie, Series
from itertools import chain
from operator import attrgetter


def home(request):
    movies = Movie.objects.filter(status='published')
    series = Series.objects.filter(status='published')
    contents = sorted(
        chain(movies, series),
        key=attrgetter('created_at'),
        reverse=True
    )
    top_rated_contents = sorted(contents, key=lambda x: float(x.score.split('/')[0]), reverse=True)[:3]

    context = {
        'top_rated_contents': top_rated_contents
    }
    return render(request, 'core/home.html', context)
