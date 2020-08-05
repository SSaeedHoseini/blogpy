from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from .validator import validate_file_extention


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='files/user_avatar', null=True, blank=True,
                              validators=[validate_file_extention])
    description = models.CharField(max_length=512, null=False, blank=False)


class Article(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    cover = models.FileField(upload_to='files/article_cover', null=False, blank=False,
                             validators=[validate_file_extention])
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    auther = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    promote = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=128,null=False, blank=False)
    cover = models.FileField(upload_to='files/category_cover/', null=False, blank=False,
                             validators=[validate_file_extention])

    def __str__(self):
        return self.title
