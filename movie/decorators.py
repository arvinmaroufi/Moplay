from django.shortcuts import redirect
from functools import wraps
from django.utils import timezone
from django.contrib import messages


def check_content_access(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # check for the existence of a slug for a movie or series
        content_slug = kwargs.get('slug') or kwargs.get('series_slug')

        if content_slug:
            try:
                from .models import Movie, Series
                from subscription.models import UserSubscription
                # first we check if it is a movie
                try:
                    content = Movie.objects.get(slug=content_slug)
                    content_type = 'movie'
                except Movie.DoesNotExist:
                    # if it weren't for the movie, we'd check out the series
                    try:
                        content = Series.objects.get(slug=content_slug)
                        content_type = 'series'
                    except Series.DoesNotExist:
                        content = None

                if content:
                    # checking the status of the content
                    if content.subscription_status == 'subscription':
                        # check if the user is logged in
                        if not request.user.is_authenticated:
                            return redirect('accounts:login')

                        # check the user's active subscription
                        active_subscription = UserSubscription.objects.filter(
                            user=request.user,
                            status='active',
                            end_date__gt=timezone.now()
                        ).exists()

                        if not active_subscription:
                            messages.error(request, 'برای دسترسی به این محتوا باید اشتراک فعال داشته باشید')
                            return redirect('subscription:plans')

            except Exception as e:
                # if an error occurs, it will redirect to the home page
                return redirect('core:home')

        return view_func(request, *args, **kwargs)

    return _wrapped_view

