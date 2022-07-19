from django.shortcuts import render, redirect
from django.views import View

from webapp.forms import ArticleForm
from webapp.models import Article


class CustomFormView(View):
    form_class = None
    template_name = None
    redirect_url = ""

    def get_redirect_url(self):
        return redirect(self.redirect_url)

    def get(self, request):
        form = self.form_class()
        context = self.get_context(form=form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_isvalid(form)

    def get_context(self, **kwargs):
        return kwargs

    def form_valid(self, form):
        return self.get_redirect_url()

    def form_isvalid(self, form):
        context = self.get_context(form=form)
        return render(self.request, self.template_name, context)


class CreateArticle(CustomFormView):
    form_class = ArticleForm
    template_name = "article_create.html"

    def form_valid(self, form):
        tags = form.cleaned_data.pop("tags")
        self.article = Article.objects.create(**form.cleaned_data)
        self.article.tags.set(tags)
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect('article_view', pk=self.article.pk)


