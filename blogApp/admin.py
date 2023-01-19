from django.contrib import admin
from parler.admin import TranslatableAdmin

from blogApp.models import UserProfile, Category, Post


class CategoryAdmin(TranslatableAdmin):
    pass

admin.site.register(UserProfile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post)
