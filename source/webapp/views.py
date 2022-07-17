from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, RedirectView

from .forms import ArticleForm
from .models import Article, STATUS_CHOICES


# def article_view(request, **kwargs):  # kwargs could be replaced directly with pk here
#     # pk = request.GET.get('pk')
#     pk = kwargs.get("pk")
#     # try:
#     #     article = Article.objects.get(pk=pk)
#     # except Article.DoesNotExist:
#     #     # return HttpResponseNotFound("Page not found")
#     #     raise Http404
#     article = get_object_or_404(Article, pk=pk)
#     return render(request, 'article_view.html', {'article': article})


class IndexView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by('-created_at')
        context = {'articles': articles}
        return render(request, "index.html", context)


class ArticleView(TemplateView):
    template_name = 'article_view.html'

    # def get_template_names(self):
    #     return "article_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        article = get_object_or_404(Article, pk=pk)
        kwargs["article"] = article
        return super().get_context_data(**kwargs)


class MyRedirectView(RedirectView):
    url = "https://google.com"


def article_create_view(request):
    if request.method == 'GET':
        form = ArticleForm()
        return render(request, 'article_create.html', {'statuses': STATUS_CHOICES, 'form': form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            content = form.cleaned_data.get('content')
            status = form.cleaned_data.get('status')
            new_art = Article.objects.create(title=title, author=author, content=content, status=status)
            return redirect('article_view', pk=new_art.pk)
        return render(request, 'article_create.html', {'form': form})



def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        form = ArticleForm(initial={
            'title': article.title,
            'author': article.author,
            'content': article.content,
            'status': article.status
        })
        return render(request, 'update.html', {'form': form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data.get('title')
            article.content = form.cleaned_data.get('content')
            article.author = form.cleaned_data.get('author')
            article.status = form.cleaned_data.get('status')
            article.save()
            return redirect('article_view', pk=article.pk)


def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', {'article': article})
    else:
        article.delete()
        return redirect('index')



