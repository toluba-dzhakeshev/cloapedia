from blog.models import Category, Post


def get_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def footer_data(request):
    recent_posts = Post.objects.all().order_by('-date_created')[:3]
    popular_posts = Post.objects.all().order_by('-rating')[:3]
    popular_categories = Category.objects.all()
    return {
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'popular_categories': popular_categories
    }
