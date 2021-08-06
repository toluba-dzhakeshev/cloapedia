from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from blog.forms import PostCreateForm
from blog.models import Post, Category


def main_page(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'blog/index.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    form = PostCreateForm()
    context = {
        'form': form
    }
    return render(request, 'blog/post_create.html', context)


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/user_posts.html', context={'posts': posts})


def category_posts(request, pk):
    category = Category.objects.filter(id=pk).first()
    posts = Post.objects.filter(category=category, published=True)
    return render(request, 'blog/category_posts.html', context={'category': category, 'posts': posts})


def search(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=query)
    return render(request, 'blog/search.html', context={'posts': posts})
