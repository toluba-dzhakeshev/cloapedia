from django.contrib import admin
from .models import Category, Post

admin.site.register(Category)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating', 'date_created', 'seen_amount', 'published']
    list_filter = ['published']
    list_editable = ['published']
