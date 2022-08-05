from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from webapp.views import ArticleView, IndexView
from webapp.views import MyRedirectView
from webapp.views import CreateArticle
from webapp.views import UpdArticle
from webapp.views import CreateCommentView
from webapp.views import UpdComment
from webapp.views import DeleteArticle
from webapp.views import DeleteComment

app_name = "webapp"


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('articles/', RedirectView.as_view(pattern_name='index')),
    path('articles/add/', CreateArticle.as_view(), name='create_article'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article_view'),
    path('article/<int:pk>/update', UpdArticle.as_view(), name='update_article'),
    path('article/<int:pk>/delete', DeleteArticle.as_view(), name='delete_article'),
    path('google/', MyRedirectView.as_view()),
    path('article/<int:pk>/comment/add/', CreateCommentView.as_view(), name='article_create_comment'),
    path('comments/<int:pk>/update', UpdComment.as_view(), name='update_comment'),
    path('comments/<int:pk>/delete', DeleteComment.as_view(), name='delete_comment'),

]
