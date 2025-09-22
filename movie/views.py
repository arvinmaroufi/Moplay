from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
