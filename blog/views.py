from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect

from blog.forms import PostCreateForm, PostUpdateForm
from blog.models import Post, Category


def main_page(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(hot_pos__isnull=False)
    context = {
        'categories': categories,
        'posts': posts,
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


def post_detail(request, pk):
    author = None
    post = Post.objects.filter(id=pk).first()
    not_anonymous = not(isinstance(request.user, AnonymousUser))
    if not_anonymous and request.user == post.author:
        pass
    else:
        post.seen_amount += 1
        post.save()

    if request.user == post.author:
        author = True

    return render(request, 'blog/post_detail.html', context={'post': post, 'author': author})


def post_update(request, pk):
    post = Post.objects.filter(id=pk).first()
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_posts')
    form = PostUpdateForm(instance=post)
    return render(request, 'blog/post_update.html', context={'post': post, 'form': form})


def post_delete(request, pk):
    post = Post.objects.filter(id=pk).first()
    post.delete()
    return redirect('my_posts')
