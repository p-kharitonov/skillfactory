# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView,  DeleteView # импортируем класс получения деталей объекта
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import PostFilter # импортируем недавно написанный фильтр
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data(**kwargs)
        post_list = PostFilter(self.request.GET, queryset=Post.objects.all()).qs
        paginator = Paginator(post_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            post_filter = paginator.page(page)
        except PageNotAnInteger:
            post_filter = paginator.page(1)
        except EmptyPage:
            post_filter = paginator.page(paginator.num_pages)
        context['filter'] = PostFilter(self.request.GET, queryset=super().get_queryset())
        context['filterset'] = post_filter
        return context


class PostUpdate(LoginRequiredMixin,UpdateView):
    template_name = 'news/create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostCreate(CreateView):
    template_name = 'news/create.html'
    form_class = PostForm


class PostDelete(DeleteView):
    template_name = 'news/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'news/post.html'  # название шаблона будет product.html
    context_object_name = 'post'  # название объекта. в нём будет