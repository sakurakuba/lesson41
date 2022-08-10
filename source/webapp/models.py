from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.urls import reverse

STATUS_CHOICES = [('new', 'brand new'), ('moderated', 'updated'), ('rejected', 'declined')]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Create date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated date')

    class Meta:
        abstract = True


class Article(BaseModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Title name')
    content = models.TextField(max_length=3000, verbose_name='Content')
    author = models.ForeignKey(get_user_model(), related_name="articles", on_delete=models.SET_DEFAULT, default=1, verbose_name="Author")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Status', default=STATUS_CHOICES[0][0])
    tags = models.ManyToManyField("webapp.Tag", related_name="articles", blank=True)

    def __str__(self):
        return f"{self.id}. {self.title}: {self.author.username}"

    def get_absolute_url(self):
        return reverse('webapp:article_view', kwargs={"pk": self.pk})



    class Meta:
        db_table = 'articles'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class Comment(BaseModel):
    text = models.TextField(max_length=400, verbose_name='Комментарий')
    author = models.ForeignKey(get_user_model(), related_name="comments", on_delete=models.SET_DEFAULT, default=1,
                               verbose_name="Author")
    article = models.ForeignKey("webapp.Article", on_delete=models.CASCADE, related_name="comments", verbose_name="article")

    def __str__(self):
        return f"{self.id}. {self.text}: {self.author.username}"

    class Meta:
        db_table = "comments"
        verbose_name = "comment"
        verbose_name_plural = "comments"


class Tag(BaseModel):
    name = models.CharField(max_length=31, verbose_name='Тег')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tags"
        verbose_name = "Tag"
        verbose_name_plural = "Tags"



