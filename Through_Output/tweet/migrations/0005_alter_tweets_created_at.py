# Generated by Django 4.2.2 on 2023-08-07 12:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0004_alter_tweets_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 7, 12, 18, 25, 622841, tzinfo=datetime.timezone.utc)),
        ),
    ]