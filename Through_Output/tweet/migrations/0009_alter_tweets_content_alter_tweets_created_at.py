# Generated by Django 4.2.2 on 2023-09-16 05:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0008_alter_tweets_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 16, 5, 46, 10, 22450, tzinfo=datetime.timezone.utc)),
        ),
    ]
