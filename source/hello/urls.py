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
from webapp.views import ArticleView, IndexView, UpdateArticle, article_create_view, delete_article

from webapp.views import MyRedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('articles/', RedirectView.as_view(pattern_name='index')),
    path('articles/add/', article_create_view, name='create_article'),
    path('article/<int:pk>/', ArticleView.as_view(extra_context={"test": "extra content"}), name='article_view'),
    path('article/<int:pk>/update', UpdateArticle.as_view(), name='update_article'),
    path('article/<int:pk>/delete', delete_article, name='delete_article'),
    path('google/', MyRedirectView.as_view())

]
