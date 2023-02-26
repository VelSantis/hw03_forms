from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .forms import PostForm
from .models import Post, Group, User


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядеть так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10) 

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
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
    # Здесь код запроса к модели и создание словаря контекста
    posts = Post.objects.filter(author__username=username).order_by("pub_date")
    post_count = Post.objects.filter(author__username=username).count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'post_count': post_count,
        'page_obj': page_obj,
        'author': User.objects.get(username=username)
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
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
        return render(request, 'posts/create_post.html', {'form': form, "is_edit": False})
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form,"is_edit": False})

    
@login_required
def post_edit(request, post_id):
    # Права на редактирование должны быть только у автора этого поста.     
    post = Post.objects.get(pk=post_id)
    if post.author.id != request.user.id:
        # Остальные пользователи должны перенаправляться на страницу просмотра поста.
        return HttpResponseRedirect(reverse('posts:post_detail', args=(post_id,)))
    if request.method == "GET":
        # При генерации страницы передайте в контекст переменную form, в ней должно быть два поля: text и group. 
        form = PostForm(instance=post)
        # Для страницы редактирования поста должен применяться тот же HTML-шаблон, что и для страницы создания нового поста: posts/create_post.html. 
        # при редактировании поста заголовок «Добавить запись» должен заменяться на «Редактировать запись»;
        return render(request, 'posts/create_post.html', {'form': form, 'is_edit': True })
    form = PostForm(request.POST)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form, 'is_edit': True })
 
    post.text = form.cleaned_data['text']
    post.group = form.cleaned_data['group'] 
    post.author = request.user
    post.save()
    return redirect('posts:post_detail', post.id)