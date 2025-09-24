from django.shortcuts import redirect
from functools import wraps


def check_content_access(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        content_slug = kwargs.get('slug') or kwargs.get('series_slug')

        if content_slug:
            try:
                from .models import Movie, Series
                try:
                    content = Movie.objects.get(slug=content_slug)
                    content_type = 'movie'
                except Movie.DoesNotExist:
                    try:
                        content = Series.objects.get(slug=content_slug)
                        content_type = 'series'
                    except Series.DoesNotExist:
                        content = None

                if content:
                    if content.subscription_status == 'subscription':
                        return redirect('core:home')

            except Exception:
                return redirect('core:home')

        return view_func(request, *args, **kwargs)

    return _wrapped_view

