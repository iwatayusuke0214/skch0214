# Generated by Django 4.2.2 on 2023-08-13 11:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweet', '0005_alter_tweets_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 13, 11, 59, 6, 643750, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweet.tweets')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tweets',
            name='likes',
            field=models.ManyToManyField(related_name='liked_tweets', through='tweet.Like', to=settings.AUTH_USER_MODEL),
        ),
    ]
