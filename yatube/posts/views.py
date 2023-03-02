from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, Group, User
from .utils import get_page_obj


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    page_obj = get_page_obj(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = get_page_obj(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    posts = Post.objects.filter(author__username=username)
    #post_count = Post.objects.filter(author__username=username).count()
    page_obj = get_page_obj(request, posts)
    context = {
        'page_obj': page_obj,
        'author': User.objects.get(username=username)
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_count = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'post_count': post_count
    }
    return render(request, 'posts/post_detail.html', context)


class PostCreate(CreateView):
    form_class = PostForm
    success_url = reverse_lazy('posts:index')
    template_name = 'posts/create_post.html'


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
        return render(request, 'posts/create_post.html',
                      {'form': form, "is_edit": False})
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html',
                  {'form': form, "is_edit": False})


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.author.id != request.user.id:
        return HttpResponseRedirect(reverse('posts:post_detail',
                                            args=(post_id,)))
    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, 'posts/create_post.html',
                      {'form': form, 'is_edit': True})
    form = PostForm(request.POST)
    if not form.is_valid():
        return render(request, 'posts/create_post.html',
                      {'form': form, 'is_edit': True})

    post.text = form.cleaned_data['text']
    post.group = form.cleaned_data['group']
    post.author = request.user
    post.save()
    return redirect('posts:post_detail', post.id)
