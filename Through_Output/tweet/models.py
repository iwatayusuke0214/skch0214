from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
from django import forms
# Create your models here.

class TweetManager(models.Manager):

    def fetch_all_themes(self):
        return self.order_by('id').all()
    

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Tweets(models.Model):
    CATEGORY_CHOICES = (
        ("FREE","FREE"),
        ("政治","政治"),
        ("IT","IT"),
        ("経済","経済"),
        ("哲学","哲学"),
        ("人間関係","人間関係"),
        ("恋愛","恋愛"),
    )

    content = models.TextField()  # ここが変更点
    # 他のフィールドやメソッド

    def __str__(self):
        return self.content[:30]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="FREE")
    user = models.ForeignKey(
        'user.Users', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now())
    likes = models.ManyToManyField(get_user_model(), through=Like, related_name='liked_tweets')

    objects = TweetManager()

    class Meta:
        db_table = 'tweets'


