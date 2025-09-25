from movie.models import Genre


def movie_func(request):
    genres_movies = Genre.objects.all()
    genres_series = Genre.objects.all()

    return {
        'genres_movies': genres_movies,
        'genres_series': genres_series,
    }
