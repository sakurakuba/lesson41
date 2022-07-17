from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from webapp.factories import ArticleFactory

from webapp.models import Article


class ArticleViewTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_art_list(self):
        ArticleFactory.create_batch(10)
        url = reverse("index")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_search_articles_list(self):
        test_art = ArticleFactory(title="Test1")
        ArticleFactory.create_batch(10)
        url = reverse("index")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(11, len(response.context.get("articles")))
        response = self.client.get(url + f"?search={test_art.title}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context.get("articles")))
        self.assertEqual(test_art.title, response.context.get("articles")[0].title)

    def test_create_article(self):
        url = reverse("create_article")
        data = {"title": "name", "author": "name", "content": "content", "status": "new"}
        response = self.client.post(url, data=data)
        self.assertEqual(302, response.status_code)
        articles = Article.objects.all()
        self.assertEqual(1, articles.count())
        self.assertEqual("name", articles.first().title)
