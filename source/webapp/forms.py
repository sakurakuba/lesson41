from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from .models import Article, STATUS_CHOICES, Tag, Comment


class ArticleForm(forms.ModelForm):
    # title = forms.CharField(max_length=50, required=True, label='Title name')
    # author = forms.CharField(max_length=50, required=True, label='Author')
    # content = forms.CharField(max_length=3000, required=False, label='Content', widget=widgets.Textarea(attrs={"cols": 15, "rows": 3}))
    # status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label='Status')
    # tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, label="Tag")

    class Meta:
        model = Article
        fields = ['title', 'content', 'status', 'tags']
        widgets = {
            "tags": widgets.CheckboxSelectMultiple,
            "content": widgets.Textarea(attrs={"placeholder": "please add text here"})
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 7:
            raise ValidationError("Error")
        return title
        
    def clean(self):
        if self.cleaned_data.get('title') == self.cleaned_data.get('content'):
            raise ValidationError("title must not match content")
        return super().clean()


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Search')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class ArticleDeleteForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title"]

    def clean_title(self):
        if self.instance.title != self.cleaned_data.get("title"):
            raise ValidationError("Title doesn't match")
        return self.cleaned_data.get("title")

