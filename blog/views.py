from django.shortcuts import render
from .models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_pages_to_show(current_page, total_pages):
    if total_pages <= 3:
        return list(range(1, total_pages + 1))

    if current_page <= 2:
        return [1, 2, 3, '...', total_pages]

    if current_page >= total_pages - 1:
        return [1, '...', total_pages - 2, total_pages - 1, total_pages]

    return [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]


def article_list(request):
    articles = Article.objects.filter(status='published').order_by('-views')

    # pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(articles, 9)
    try:
        object_list = paginator.page(page_number)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'articles': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'blog/article_list.html', context)
