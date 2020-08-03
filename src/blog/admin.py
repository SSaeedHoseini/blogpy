from django.contrib import admin
from .models import *


class UserProfielAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover', ]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover', 'created_at', ]
    search_fields = ['title', 'content', ]


admin.site.register(UserProfile, UserProfielAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
