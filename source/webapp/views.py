from django.shortcuts import render


# Create your views here.
from .models import Article, STATUS_CHOICES


def article_view(request):
    pk = request.GET.get('pk')
    article = Article.objects.get(pk=pk)
    return render(request, 'article_view.html', {'article': article})


def index_view(request):
    articles = Article.objects.order_by('-created_at')
    context = {'articles': articles}
    # print(request.GET)
    # print(request.GET.getlist('my_param'))
    # print(request.GET.get('my_param', 10))
    # print(request.GET.get('other_param'))
    # print(request.GET.get('other_param', 10))
    return render(request, "index.html", context)


def article_create_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html', {'statuses': STATUS_CHOICES})
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        status = request.POST.get('status')
        author = request.POST.get('author')
        new_art = Article.objects.create(title=title, author=author, content=content, status=status)
        context = {'article': new_art}
        return render(request, 'article_view.html', context)







