from django.shortcuts import render
from .models import Page
from django.views.generic import ListView, DetailView, CreateView, UpdateView,  DeleteView


class HomeView(ListView):
    model = Page
    template_name = 'page/home.html'
    context_object_name = 'pages'
    # ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PageListView(ListView):
    model = Page
    template_name = 'page/pages.html'
    context_object_name = 'pages'
    # ordering = ['-created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = 'page/page.html'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
