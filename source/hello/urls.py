"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from webapp.views import ArticleView, IndexView, delete_article
from webapp.views import MyRedirectView
from webapp.views import CreateArticle
from webapp.views import UpdArticle
from webapp.views import CreateCommentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('articles/', RedirectView.as_view(pattern_name='index')),
    path('articles/add/', CreateArticle.as_view(), name='create_article'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article_view'),
    path('article/<int:pk>/update', UpdArticle.as_view(), name='update_article'),
    path('article/<int:pk>/delete', delete_article, name='delete_article'),
    path('google/', MyRedirectView.as_view()),
    path('article/<int:pk>/comment/add/', CreateCommentView.as_view(), name='article_create_comment'),

]
