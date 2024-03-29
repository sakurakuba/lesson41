from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, RedirectView, FormView, ListView, DetailView, CreateView, UpdateView, \
    DeleteView

from .base_view import CustomFormView, CustomListView
from .forms import ArticleForm, SearchForm, CommentForm, ArticleDeleteForm
from .models import Article, Comment


class IndexView(ListView):
    model = Article
    template_name = "index.html"
    context_object_name = "articles"
    ordering = ('created_at',)
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        # request.user.user_permissions.add(Permission.objects.get(codename="delete_article"))
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Article.objects.filter(Q(author__contains=self.search_value) | Q(title__contains=self.search_value))
        return Article.objects.order_by('-created_at')

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


class ArticleView(DetailView):
    template_name = 'article_view.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        return context


class MyRedirectView(RedirectView):
    url = "https://google.com"


class CreateArticle(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = "article_create.html"
    #permission_required = "webapp.add_article"
    #
    # def has_permission(self):
    #     return self.request.user.has_perm("webapp.add_article")
    #
    # def handle_no_permission(self):
    #     return redirect("accounts:login")

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and self.request.user.has_perm("webapp.add_article"):
    #         return super().dispatch(request, *args, **kwargs)
    #     return redirect("accounts:login")

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        return super().form_valid(form)


class UpdArticle(PermissionRequiredMixin, UpdateView):
    form_class = ArticleForm
    template_name = "update.html"
    model = Article

    def has_permission(self):
        return self.request.user.has_perm("webapp.change_article") or \
               self.request.user == self.get_object().author



class DeleteArticle(PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = "delete.html"
    success_url = reverse_lazy("webapp:index")
    form_class = ArticleDeleteForm
    permission_required = "webapp.delete_article"

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.get_object())
        if form.is_valid():
            return self.delete(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)






class CreateCommentView(CreateView):
    form_class = CommentForm
    template_name = "comments/create_comment.html"

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs.get("pk"))
        user = self.request.user
        form.instance.article = article
        form.instance.author = user
        return super().form_valid(form)

    # def form_valid(self, form):
    #     article = get_object_or_404(Article, pk=self.kwargs.get("pk"))
    #     comment = form.save(commit=False)
    #     comment.article = article
    #     comment.save()
    #     form.save_m2m()
    #     return redirect("article_view", pk=article.pk)

    def get_success_url(self):
        return reverse("webapp:article_view", kwargs={"pk": self.object.article.pk})


class UpdComment(UserPassesTestMixin, UpdateView):
    form_class = CommentForm
    template_name = "comments/update.html"
    model = Comment

    def test_func(self):
        return self.get_object().author == self.request.user or self.request.user.has_perm('webapp.change_comment')

    def get_success_url(self):
        return reverse("webapp:article_view", kwargs={"pk": self.object.article.pk})


class DeleteComment(DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("webapp:article_view", kwargs={"pk": self.object.article.pk})
