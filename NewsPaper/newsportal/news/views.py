# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView,  DeleteView # импортируем класс получения деталей объекта
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Post, Author
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import PostFilter # импортируем недавно написанный фильтр
from .forms import PostForm



class HomeView(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_post'] = Post.objects.all().count()
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostListView(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_post'] = Post.objects.all().count()
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['post_author'] = str(Post.objects.get(pk=self.kwargs.get('pk')).author.user)
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['count_post'] = PostFilter(self.request.GET, queryset=self.get_queryset()).qs.count()
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        word = PostFilter(self.request.GET, queryset=qs)
        return word.qs


class PostAdd(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'news/post_add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        form.instance.author = Author.objects.get(user=self.request.user)
        return super(PostAdd, self).form_valid(form)


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'news/post_update.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.user
        user = User.objects.get(username=self.request.user)
        if user != author:
            raise PermissionDenied
        return Post.objects.get(pk=self.kwargs.get('pk'))


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post',)

    def get_object(self, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.user
        user = User.objects.get(username=self.request.user)
        if user != author:
            raise PermissionDenied
        return Post.objects.get(pk=self.kwargs.get('pk'))


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    if not Author.objects.filter(user=user).exists():
        Author.objects.create(user=user)
    return redirect('/')