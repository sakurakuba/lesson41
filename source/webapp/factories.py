import factory
import factory.fuzzy

from webapp.models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Faker("sentence")
    author = factory.Faker("name")
    content = factory.Faker("text")
    status = factory.fuzzy.FuzzyChoice(choices=['new', 'moderated', 'rejected'])

