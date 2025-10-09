from django.shortcuts import render, redirect
from movie.models import Movie, Series
from itertools import chain
from operator import attrgetter
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ContactForm
from django.utils import timezone
from datetime import timedelta


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
    # top_rated contents
    movies = Movie.objects.filter(status='published')
    series = Series.objects.filter(status='published')
    contents = sorted(chain(movies, series), key=attrgetter('created_at'), reverse=True)
    top_rated_contents = sorted(contents, key=lambda x: float(x.score.split('/')[0]), reverse=True)[:3]

    # suggestion contents
    suggestion_movies = Movie.objects.filter(status='published', is_recommended=True)[:5]
    suggestion_series = Series.objects.filter(status='published', is_recommended=True)[:5]
    suggestion_contents = sorted(chain(suggestion_movies, suggestion_series), key=attrgetter('created_at'), reverse=True)

    # latest movies
    thirty_days_ago = timezone.now() - timedelta(days=30)
    latest_movies = Movie.objects.filter(created_at__gte=thirty_days_ago, status='published').order_by('-created_at')[:6]

    # popular movies
    popular_movies = Movie.objects.filter(status='published').order_by('-views')[:10]

    # latest series
    latest_series = Series.objects.filter(created_at__gte=thirty_days_ago, status='published').order_by('-created_at')[:6]

    # popular series
    popular_series = Series.objects.filter(status='published').order_by('-views')[:10]

    context = {
        'top_rated_contents': top_rated_contents,
        'suggestion_contents': suggestion_contents,
        'latest_movies': latest_movies,
        'popular_movies': popular_movies,
        'latest_series': latest_series,
        'popular_series': popular_series,
    }
    return render(request, 'core/home.html', context)


def search_results(request):
    query = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)

    if query:
        movies = Movie.objects.filter(Q(title__icontains=query), status='published')
        series = Series.objects.filter(Q(title__icontains=query), status='published')
        items = list(movies) + list(series)

        # pagination
        paginator = Paginator(items, 15)
        try:
            object_list = paginator.page(page_number)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    else:
        items = []
        object_list = Paginator(items, 15).get_page(1)
        pages_to_show = []

    context = {
        'query': query,
        'items': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'core/search_results.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    else:
        form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'core/contact.html', context)


def about(request):
    return render(request, 'core/about.html')


def terms(request):
    return render(request, 'core/terms.html')
