# Generated by Django 4.0.5 on 2022-07-03 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('new', 'brand new'), ('moderated', 'updated'), ('rejected', 'declined')], default='new', max_length=20, verbose_name='Status'),
        ),
    ]
