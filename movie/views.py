from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from itertools import chain
from operator import attrgetter
from .decorators import check_content_access
from django.contrib.auth.decorators import login_required


def get_pages_to_show(current_page, total_pages):
    if total_pages <= 3:
        return list(range(1, total_pages + 1))

    if current_page <= 2:
        return [1, 2, 3, '...', total_pages]

    if current_page >= total_pages - 1:
        return [1, '...', total_pages - 2, total_pages - 1, total_pages]

    return [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]


def movies_list(request):
    movies = Movie.objects.filter(status='published').order_by('-views')

    # filters

    # filter by search
    search_query = request.GET.get('search', '')
    if search_query:
        movies = movies.filter(Q(title__icontains=search_query))

    # filter by genre
    genre_filter = request.GET.getlist('genre')
    if genre_filter:
        movies = movies.filter(genre__id__in=genre_filter).distinct()

    # filter by year
    year_filter = request.GET.getlist('year')
    if year_filter:
        movies = movies.filter(release_date__year__in=year_filter)

    # filter by country
    country_filter = request.GET.getlist('country')
    if country_filter:
        movies = movies.filter(country__id__in=country_filter).distinct()

    # filter by dubbing/subtitle status
    dubbed_filter = request.GET.get('dubbed_or_subtitle', '')
    if dubbed_filter:
        movies = movies.filter(dubbed_or_subtitle=dubbed_filter)

    # filter by subscription status
    subscription_filter = request.GET.get('subscription_status', '')
    if subscription_filter:
        movies = movies.filter(subscription_status=subscription_filter)

    # sorting
    sort_by = request.GET.get('sort', '')
    if sort_by == 'newest':
        movies = movies.order_by('-created_at')
    elif sort_by == 'oldest':
        movies = movies.order_by('created_at')
    elif sort_by == 'highest_views':
        movies = movies.order_by('-views')
    elif sort_by == 'highest_score':
        movies = movies.order_by('-score')

    # pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(movies, 15)
    try:
        object_list = paginator.page(page_number)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    # Get all genres, years, and countries to display in the filter
    all_genres = Genre.objects.all()
    all_years = Year.objects.all().order_by('-year')
    all_countries = Country.objects.all()

    context = {
        'movies': object_list,
        'pages_to_show': pages_to_show,
        'all_genres': all_genres,
        'all_years': all_years,
        'all_countries': all_countries,
        'current_filters': request.GET,
    }
    return render(request, 'movie/movies_list.html', context)


def series_list(request):
    series = Series.objects.filter(status='published').order_by('-views')

    # filters

    # filter by search
    search_query = request.GET.get('search', '')
    if search_query:
        series = series.filter(Q(title__icontains=search_query))

    # filter by genre
    genre_filter = request.GET.getlist('genre')
    if genre_filter:
        series = series.filter(genre__id__in=genre_filter).distinct()

    # filter by year
    year_filter = request.GET.getlist('year')
    if year_filter:
        series = series.filter(release_date__year__in=year_filter)

    # filter by country
    country_filter = request.GET.getlist('country')
    if country_filter:
        series = series.filter(country__id__in=country_filter).distinct()

    # filter by dubbing/subtitle status
    dubbed_filter = request.GET.get('dubbed_or_subtitle', '')
    if dubbed_filter:
        series = series.filter(dubbed_or_subtitle=dubbed_filter)

    # filter by subscription status
    subscription_filter = request.GET.get('subscription_status', '')
    if subscription_filter:
        series = series.filter(subscription_status=subscription_filter)

    # sorting
    sort_by = request.GET.get('sort', '')
    if sort_by == 'newest':
        series = series.order_by('-created_at')
    elif sort_by == 'oldest':
        series = series.order_by('created_at')
    elif sort_by == 'highest_views':
        series = series.order_by('-views')
    elif sort_by == 'highest_score':
        series = series.order_by('-score')

    # pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(series, 15)
    try:
        object_list = paginator.page(page_number)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    # Get all genres, years, and countries to display in the filter
    all_genres = Genre.objects.all()
    all_years = Year.objects.all().order_by('-year')
    all_countries = Country.objects.all()

    context = {
        'series': object_list,
        'pages_to_show': pages_to_show,
        'all_genres': all_genres,
        'all_years': all_years,
        'all_countries': all_countries,
        'current_filters': request.GET,
    }
    return render(request, 'movie/series_list.html', context)


def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug, status='published')
    movie.views += 1
    movie.save()

    if request.method == 'POST':
        content = request.POST.get('content')
        if content and content.strip():
            MovieComment.objects.create(content=content, movie=movie, author=request.user)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponse('OK')

        return redirect('movie:movie_detail', slug=slug)

    # similar movies and series
    movies = Movie.objects.filter(genre__in=movie.genre.all(), status='published').exclude(id=movie.id).distinct()[:5]
    series = Series.objects.filter(genre__in=movie.genre.all(), status='published').distinct()[:5]
    similar_contents = sorted(
        chain(movies, series),
        key=attrgetter('created_at'),
        reverse=True
    )

    context = {
        'movie': movie,
        'similar_contents': similar_contents,
    }
    return render(request, 'movie/movie_detail.html', context)


def series_detail(request, slug):
    series = get_object_or_404(Series, slug=slug, status='published')
    series.views += 1
    series.save()
    chapters = series.chapterseries_set.all()

    if request.method == 'POST':
        content = request.POST.get('content')
        if content and content.strip():
            SeriesComment.objects.create(content=content, series=series, author=request.user)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponse('OK')

        return redirect('movie:series_detail', slug=slug)

    # similar movies and series
    m = Movie.objects.filter(genre__in=series.genre.all(), status='published').distinct()[:5]
    s = Series.objects.filter(genre__in=series.genre.all(), status='published').exclude(id=series.id).distinct()[:5]
    similar_contents = sorted(
        chain(m, s),
        key=attrgetter('created_at'),
        reverse=True
    )

    context = {
        'series': series,
        'chapters': chapters,
        'similar_contents': similar_contents,
    }
    return render(request, 'movie/series_detail.html', context)


@check_content_access
@login_required
def movie_watch(request, slug):
    movie = get_object_or_404(Movie, slug=slug, status='published')

    context = {
        'movie': movie,
    }
    return render(request, 'movie/movie_watch.html', context)


@check_content_access
@login_required
def series_watch(request, series_slug, video_id):
    series = get_object_or_404(Series, slug=series_slug, status='published')
    video = get_object_or_404(VideoSeries, id=video_id, chapter__series=series)

    context = {
        'video': video,
        'series': series,
    }
    return render(request, 'movie/series_watch.html', context)


@check_content_access
@login_required
def series_download(request, series_slug, quality):
    series = get_object_or_404(Series, slug=series_slug, status='published')
    chapters = ChapterSeries.objects.filter(series=series).prefetch_related('videoseries_set')

    valid_qualities = ['480p', '720p', '1080p']
    if quality not in valid_qualities:
        quality = '480p'

    context = {
        'series': series,
        'chapters': chapters,
        'quality': quality,
        'available_qualities': valid_qualities,
    }
    return render(request, 'movie/series_download.html', context)


def genre_movies(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    movies = genre.movies_genre.filter(status='published')

    # pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(movies, 15)
    try:
        object_list = paginator.page(page_number)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'genre': genre,
        'movies': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'movie/genre_movies.html', context)


def genre_series(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    series = genre.series_genre.filter(status='published')

    # pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(series, 15)
    try:
        object_list = paginator.page(page_number)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'genre': genre,
        'series': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'movie/genre_series.html', context)


def directors_list(request):
    directors = Director.objects.all().order_by('-created_at')

    page_number = request.GET.get('page', 1)
    paginator = Paginator(directors, 15)
    try:
        object_list = paginator.page(page_number)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'directors': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'movie/directors_list.html', context)


def director_detail(request, slug):
    director = get_object_or_404(Director, slug=slug)

    movies = Movie.objects.filter(director=director, status='published')
    series = Series.objects.filter(director=director, status='published')
    contents = sorted(
        chain(movies, series),
        key=attrgetter('created_at'),
        reverse=True
    )

    context = {
        'director': director,
        'movies': movies,
        'series': series,
        'contents': contents,
    }
    return render(request, 'movie/director_detail.html', context)


def actors_list(request):
    actors = Actor.objects.all().order_by('-created_at')

    page_number = request.GET.get('page', 1)
    paginator = Paginator(actors, 15)
    try:
        object_list = paginator.page(page_number)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'actors': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'movie/actors_list.html', context)


def actor_detail(request, slug):
    actor = get_object_or_404(Actor, slug=slug)

    movies = Movie.objects.filter(actors=actor, status='published')
    series = Series.objects.filter(actors=actor, status='published')

    contents = sorted(
        chain(movies, series),
        key=attrgetter('created_at'),
        reverse=True
    )

    context = {
        'actor': actor,
        'movies': movies,
        'series': series,
        'contents': contents,
    }
    return render(request, 'movie/actor_detail.html', context)
