from django import forms
from django.forms import widgets

from .models import Article, STATUS_CHOICES


class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=50, required=True, label='Title name')
    author = forms.CharField(max_length=50, required=True, label='Author')
    content = forms.CharField(max_length=3000, required=False, label='Content', widget=widgets.Textarea(attrs={"cols": 15, "rows": 3}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label='Status')

    class Meta:
        model = Article
        fields = "__all__"


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Search')
