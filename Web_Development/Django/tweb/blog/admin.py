from django.contrib import admin

# Register your models here.

from .models import Article, Test

admin.site.register(Article)

admin.site.register(Test)