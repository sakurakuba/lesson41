from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse

# Create your views here.
from django.views import View

from .models import Article, STATUS_CHOICES


def article_view(request, **kwargs):  # kwargs could be replaced directly with pk here
    # pk = request.GET.get('pk')
    pk = kwargs.get("pk")
    # try:
    #     article = Article.objects.get(pk=pk)
    # except Article.DoesNotExist:
    #     # return HttpResponseNotFound("Page not found")
    #     raise Http404
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_view.html', {'article': article})


class IndexView(View):
    def get(self, request, *args, **kwargs):
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
        ## status = request.POST.get('status')
        author = request.POST.get('author')
        new_art = Article.objects.create(title=title, author=author, content=content)  # status=status)
        context = {'article': new_art}
        ## return HttpResponseRedirect(f"/article/{new_art.pk}")
        # return render(request, 'article_view.html', context)
        ### return HttpResponseRedirect(reverse('article_view', kwargs={'pk': new_art.pk}))
        return redirect('article_view', pk=new_art.pk)

def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'update.html', {'article': article})
    else:
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.author = request.POST.get('author')
        article.save()
        return redirect('article_view', pk=article.pk)

def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', {'article': article})
    else:
        article.delete()
        return redirect('index')



