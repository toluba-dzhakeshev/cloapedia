from django.urls import path
from .views import main_page, create_post, my_posts, category_posts, search, post_detail, post_update, post_delete

urlpatterns = [
    path('post-delete/<int:pk>/', post_delete, name='post_delete'),
    path('post-update/<int:pk>/', post_update, name='post_update'),
    path('post-detail/<int:pk>/', post_detail, name='post_detail'),
    path('category/<int:pk>/', category_posts, name='category_details'),
    path('my-posts/', my_posts, name='my_posts'),
    path('create-post/', create_post, name='post_create'),
    path('search/', search, name='search'),
    path('', main_page, name='main_page'),
]
