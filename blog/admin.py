from django.contrib import admin
from .models import Category, Post

admin.site.register(Category)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating', 'date_created', 'seen_amount', 'published', 'hot_pos']
    list_filter = ['published', 'hot_pos']
    list_editable = ['published']
