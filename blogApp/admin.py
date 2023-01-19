import django
from django.contrib import admin
from blogApp.models import UserProfile, Category, Post

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Post)
