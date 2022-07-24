from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import ArticleForm
from webapp.models import Article


class DetailView(TemplateView):
    context_key = 'object'
    model = None
    key_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_key] = self.get_object()
        return context

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)


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



class CustomListView(TemplateView):
    model = None
    context_key = "objects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_key] = self.get_objects()
        return context

    def get_objects(self):
        return self.model.objects.all()




