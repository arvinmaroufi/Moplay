from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Tag
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


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    article.views += 1
    article.save()

    categories = Category.objects.all()
    popular_tags = Tag.objects.all().order_by('-views')[:9]
    recent_articles = Article.objects.filter(status='published').exclude(slug=slug).order_by('-created_at')[:3]

    context = {
        'article': article,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_articles': recent_articles,
    }
    return render(request, 'blog/article_detail.html', context)


def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.filter(status='published').order_by('-views')

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
        'category': category,
        'articles': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'blog/category_articles.html', context)


def tag_articles(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    tag.views += 1
    tag.save()

    articles = tag.articles.filter(status='published').order_by('-views')

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
        'tag': tag,
        'articles': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'blog/tag_articles.html', context)
