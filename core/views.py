from django.shortcuts import render, redirect
from movie.models import Movie, Series
from itertools import chain
from operator import attrgetter


def redirect_to_home(request):
    return redirect('core:home')


def get_pages_to_show(current_page, total_pages):
    if total_pages <= 3:
        return list(range(1, total_pages + 1))

    if current_page <= 2:
        return [1, 2, 3, '...', total_pages]

    if current_page >= total_pages - 1:
        return [1, '...', total_pages - 2, total_pages - 1, total_pages]

    return [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]


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
