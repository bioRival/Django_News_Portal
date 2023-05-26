from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = '-publication_date'
    queryset = Post.objects.filter(type='N') # Filter for returting only News from posts
    template_name = 'news.html'
    context_object_name = 'news_list'


class PostsList(ListView):
    model = Post
    template_name = 'flatpages/index.html'
    context_object_name = 'posts_list'

    def get_queryset(self, *args, **kwargs):
        qs = super(PostsList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-rating")
        qs = qs.all()[:3]
        return qs

class NewsDetail(DetailView):
    model = Post
    template_name = 'news_page.html'
    context_object_name = 'news_page'