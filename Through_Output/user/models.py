from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager
from django.contrib.staticfiles.storage import staticfiles_storage
# Create your models here.

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, blank=True, upload_to='picture/', default='picture/default.jpeg')
    profile = models.CharField(max_length=200, blank=True, default="")
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def picture_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        return staticfiles_storage.url('picture/default.jpeg')

    class Meta:
        db_table = 'users'


class UserActivateTokensManager(models.Manager):

    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        user = user_activate_token.user
        user.is_active = True
        user.save()


class UserActivateTokens(models.Model):

    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )

    objects = UserActivateTokensManager()

    class Meta:
        db_table = 'user_activate_tokens'