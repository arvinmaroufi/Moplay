from movie.models import Genre, Tag


def movie_func(request):
    genres_movies = Genre.objects.all()
    genres_series = Genre.objects.all()
    popular_tags = Tag.objects.all().order_by('-views')[:20]

    return {
        'genres_movies': genres_movies,
        'genres_series': genres_series,
        'popular_tags': popular_tags,
    }
