from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from core.views import redirect_to_home, search_results

urlpatterns = [
    # redirect urls
    path('genre/', redirect_to_home, name='redirect_to_home'),
    path('genre/movies/', redirect_to_home, name='redirect_to_home'),
    path('genre/series/', redirect_to_home, name='redirect_to_home'),
    path('tag/', redirect_to_home, name='redirect_to_home'),
    path('language/', redirect_to_home, name='redirect_to_home'),
    path('year/', redirect_to_home, name='redirect_to_home'),
    path('country/', redirect_to_home, name='redirect_to_home'),
    path('articles/category/', redirect_to_home, name='redirect_to_home'),

    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('movie.urls')),
    path('', include('subscription.urls')),
    path('', include('blog.urls')),

    # search url
    path('/', search_results, name='search_results'),

    # ckeditor url
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
