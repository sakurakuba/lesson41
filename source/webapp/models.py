from django.db import models

# Create your models here.
STATUS_CHOICES = [('new', 'brand new'), ('moderated', 'updated'), ('rejected', 'declined')]


class Article(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Title name')
    author = models.CharField(max_length=50, verbose_name='Author', default='Unknown')
    content = models.TextField(max_length=3000, verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Create date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated date')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Status', default=STATUS_CHOICES[0][0])

    def __str__(self):
        return f"{self.id}. {self.title}: {self.author}"

    class Meta:
        db_table = 'articles'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
