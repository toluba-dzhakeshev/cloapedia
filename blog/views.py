from functools import reduce

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from blog.forms import PostCreateForm, PostUpdateForm, CommentForm
from blog.models import Post, Category, Rating


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
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/user_posts.html', context={'posts': page_obj})


def category_posts(request, pk):
    category = Category.objects.filter(id=pk).first()
    posts = Post.objects.filter(category=category, published=True)
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category_posts.html', context={'category': category, 'posts': page_obj})


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

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user
            comment.save()

    form = CommentForm()
    context = {
        'post': post,
        'author': author,
        'form': form
    }

    return render(request, 'blog/post_detail.html', context)


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


def rate_post(request, pk, rate):
    post = Post.objects.filter(id=pk).first()

    not_anonymous = not (isinstance(request.user, AnonymousUser))
    try:
        rated_before = Rating.objects.filter(profile=request.user, post=post).first()
    except TypeError:
        messages.error(request, 'You cannot rate. Login first')
        return redirect('main_page')

    if request.user and not_anonymous and not rated_before:
        messages.success(request, 'Your rating has been saved')
        rating = Rating(
            post=post, profile=request.user,
            rate=rate, rated=True
        )
        rating.save()
    else:
        messages.error(request, 'You have already rated before')
        return redirect('main_page')

    rates = Rating.objects.filter(post=post)

    stars = reduce(lambda x, y: x + y, [i.rate for i in rates])
    post.rating = stars/len(rates)
    post.save()
    return redirect('main_page')
