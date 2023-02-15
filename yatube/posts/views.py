from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


from .forms import PostForm
from .models import Post, Group


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    posts = Post.objects.filter(author__username=username)
    post_count = Post.objects.filter(author__username=username).count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
        'post_count': post_count,
        'page_obj': page_obj
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
            print(request.user)
            print(type(request.user))
            print(request.user.id)
            post.author = request.user
            post.save()
            #form.save()
            #return redirect('posts:profile', request.user)
        return render(request, 'posts/create_post.html', {'form': form,})
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form,})

    
def post_edit(request):
    return render(request, '/posts/<post_id>/edit/')
