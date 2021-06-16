# from django.shortcuts import render
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView,  DeleteView # импортируем класс получения деталей объекта
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Post, Author, Category
from .filters import PostFilter # импортируем недавно написанный фильтр
from .forms import PostForm
from .tasks import notify_users


class HomeView(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_post'] = Post.objects.all().count()
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
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


class PostSearchView(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['count_post'] = PostFilter(self.request.GET, queryset=self.get_queryset()).qs.count()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        word = PostFilter(self.request.GET, queryset=qs)
        return word.qs


class PostAddView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'news/post_add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def get(self, request, *args, **kwargs):
        author = Author.objects.get(user=self.request.user)
        now = datetime.now()
        today = now.date()
        count_post = Post.objects.filter(author=author, created_at__gte=today).count()
        print(count_post)
        if count_post >= 3:
            raise PermissionDenied("Вы не можете оставлять более 3 статей в день!")
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        author = Author.objects.get(user=self.request.user)
        today = datetime.today().date()
        count_post = Post.objects.filter(author=author, created_at__gte=today).count()
        print(count_post)
        if count_post >= 3:
            raise PermissionDenied("Вы не можете оставлять более 3 статей в день!")
        self.object = None
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = Author.objects.get(user=self.request.user)
        post = form.save()
        notify_users.delay(post.pk)
        return redirect('post', pk=post.pk)


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'news/post_update.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.user
        user = User.objects.get(username=self.request.user)
        if user != author:
            raise PermissionDenied
        return Post.objects.get(pk=self.kwargs.get('pk'))


class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
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


class CategoriesListView(ListView):
    template_name = 'news/categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()


class PostsCategoryListView(ListView):
    model = Post
    template_name = 'news/posts_of_category.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        pk = self.kwargs['pk']
        category = Category.objects.get(id=pk)
        return qs.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        category = Category.objects.get(id=pk)
        context['pk'] = pk
        context['category'] = category
        context['count_post'] = Post.objects.filter(category=category).count()
        context['is_not_subscriber'] = self.request.user not in category.subscribers.all()
        return context


@login_required
def subscribe(request):
    if request.POST:
        pk = request.POST.get('pk')
        category = Category.objects.get(pk=pk)
        if request.user not in category.subscribers.all():
            category.subscribers.add(request.user)
        else:
            category.subscribers.remove(request.user)
        return redirect('posts_category', pk=pk)
    else:
        return redirect('home')