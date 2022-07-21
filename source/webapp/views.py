from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, RedirectView, FormView, ListView

from .base_view import CustomFormView, CustomListView
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


# class IndexView(View):
#     def get(self, request, *args, **kwargs):
#         search_form = SearchForm(data=request.GET)
#         articles = Article.objects.all()
#         if search_form.is_valid():
#             search_value = search_form.cleaned_data.get("search")
#             articles = articles.filter(title__contains=search_value)
#         articles = articles.order_by('-created_at')
#         context = {'articles': articles, 'form': search_form}
#         return render(request, "index.html", context)


class IndexView(ListView):
    model = Article
    template_name = "index.html"
    context_object_name = "articles"
    ordering = ('created_at',)
    paginate_by = 2


    # def get_objects(self):
    #    # return super().get_objects().order_by('-created_at')
    #     return Article.objects.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Article.objects.filter(Q(author__contains=self.search_value) | Q(title__contains=self.search_value))
        return Article.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            val = urlencode({'search': self.search_value})
            context['query'] = val
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")




class ArticleView(TemplateView):
    template_name = 'article_view.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        article = get_object_or_404(Article, pk=pk)
        kwargs["article"] = article
        return super().get_context_data(**kwargs)


class MyRedirectView(RedirectView):
    url = "https://google.com"


# def article_create_view(request):
#     if request.method == 'GET':
#         form = ArticleForm()
#         return render(request, 'article_create.html', {'form': form})
#     else:
#         form = ArticleForm(data=request.POST)
#         if form.is_valid():
#             tags = form.cleaned_data.pop("tags")
#             title = form.cleaned_data.get('title')
#             author = form.cleaned_data.get('author')
#             content = form.cleaned_data.get('content')
#             status = form.cleaned_data.get('status')
#             new_art = Article.objects.create(title=title, author=author, content=content, status=status)
#             new_art.tags.set(tags)
#             return redirect('article_view', pk=new_art.pk)
#         return render(request, 'article_create.html', {'form': form})


class CreateArticle(CustomFormView):
    form_class = ArticleForm
    template_name = "article_create.html"

    def form_valid(self, form):
        # tags = form.cleaned_data.pop("tags")
        # self.article = Article.objects.create(**form.cleaned_data)
        # self.article.tags.set(tags)
        self.article = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect('article_view', pk=self.article.pk)


class UpdArticle(FormView):
    form_class = ArticleForm
    template_name = "update.html"

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        return context

    def get_success_url(self):
        return reverse("article_view", kwargs={"pk": self.article.pk})

    def get_object(self):
        return get_object_or_404(Article, pk=self.kwargs.get('pk'))

    # def get_initial(self):
    #     initial = {}
    #     for key in 'title', 'content', 'author', 'status':
    #         initial[key] = getattr(self.article, key)
    #     initial['tags'] = self.article.tags.all()
    #     return initial

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['instance'] = self.article
        return form_kwargs

    def form_valid(self, form):
        tags = form.cleaned_data.pop('tags')
        # ##self.article.objects.update(**form.cleaned_data)
        # for key, value in form.cleaned_data.items():
        #     setattr(self.article, key, value)
        self.article = form.save()
        ##self.article.tags.set(tags)
        return super().form_valid(form)





# class UpdateArticle(View):
#     def dispatch(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         self.article = get_object_or_404(Article, pk=pk)
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             form = ArticleForm(initial={
#                 'title': self.article.title,
#                 'author': self.article.author,
#                 'content': self.article.content,
#                 'status': self.article.status,
#                 'tags': self.article.tags.all()
#             })
#             return render(request, 'update.html', {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = ArticleForm(data=request.POST)
#         if form.is_valid():
#             self.article.title = form.cleaned_data.get('title')
#             self.article.content = form.cleaned_data.get('content')
#             self.article.author = form.cleaned_data.get('author')
#             self.article.status = form.cleaned_data.get('status')
#             self.article.tags.set(form.cleaned_data.get('tags'))
#             self.article.save()
#             return redirect('article_view', pk=self.article.pk)
#         return render(request, 'update.html', {'form': form})


def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', {'article': article})
    else:
        article.delete()
        return redirect('index')



