from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, RedirectView

from .forms import ArticleForm, SearchForm
from .models import Article


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
        search_form = SearchForm(data=request.GET)
        articles = Article.objects.all()
        if search_form.is_valid():
            search_value = search_form.cleaned_data.get("search")
            articles = articles.filter(title__contains=search_value)
        articles = articles.order_by('-created_at')
        context = {'articles': articles, 'form': search_form}
        return render(request, "index.html", context)


class ArticleView(TemplateView):
    template_name = 'article_view.html'

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
        return render(request, 'article_create.html', {'form': form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            tags = form.cleaned_data.pop("tags")
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            content = form.cleaned_data.get('content')
            status = form.cleaned_data.get('status')
            new_art = Article.objects.create(title=title, author=author, content=content, status=status)
            new_art.tags.set(tags)
            return redirect('article_view', pk=new_art.pk)
        return render(request, 'article_create.html', {'form': form})


class UpdateArticle(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        self.article = get_object_or_404(Article, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = ArticleForm(initial={
                'title': self.article.title,
                'author': self.article.author,
                'content': self.article.content,
                'status': self.article.status,
                'tags': self.article.tags.all()
            })
            return render(request, 'update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            self.article.title = form.cleaned_data.get('title')
            self.article.content = form.cleaned_data.get('content')
            self.article.author = form.cleaned_data.get('author')
            self.article.status = form.cleaned_data.get('status')
            self.article.tags.set(form.cleaned_data.get('tags'))
            self.article.save()
            return redirect('article_view', pk=self.article.pk)
        return render(request, 'update.html', {'form': form})


def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', {'article': article})
    else:
        article.delete()
        return redirect('index')



