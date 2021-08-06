from django.urls import path
from .views import main_page, create_post, my_posts, category_posts, search

urlpatterns = [
    path('category/<int:pk>/', category_posts, name='category_details'),
    path('my-posts/', my_posts, name='my_posts'),
    path('create-post/', create_post, name='post_create'),
    path('search/', search, name='search'),
    path('', main_page, name='main_page'),
]
