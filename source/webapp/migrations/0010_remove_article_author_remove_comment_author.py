# Generated by Django 4.0.5 on 2022-08-09 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_remove_article_tags_old_delete_articletag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
    ]