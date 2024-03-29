from django.contrib import admin
from webapp.models import Article
# Register your models here.

# class TagInline(admin.TabularInline):
#     model = Article.tags.through


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    list_display_links = ['title']
    list_filter = ['author']
    search_fields = ['title', 'content']
    fields = ['title', 'author', 'content', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    # inlines = [TagInline]

#
# # class TagsAdmin(admin.ModelAdmin):
# #     inlines = [TagInline]
#
#
#
# # admin.site.register(Tags, TagsAdmin)
admin.site.register(Article, ArticleAdmin)
