# Generated by Django 4.2.2 on 2023-07-25 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 25, 15, 19, 42, 648608, tzinfo=datetime.timezone.utc)),
        ),
    ]
