from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .filters import PostFilter


class NewsList(ListView):
    model = Post
    ordering = '-publication_date'
    queryset = Post.objects.filter(type='N') # Filter for returting only News from posts
    template_name = 'news.html'
    context_object_name = 'news_list'
    paginate_by = 10


class SearchNewsList(ListView):
    model = Post
    ordering = '-publication_date'
    queryset = Post.objects.filter(type='N')  # Filter for returting only News from posts
    template_name = 'search_news.html'
    context_object_name = 'search_news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


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


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        if "news" in self.request.path.split("/"):
            post.type = "N"
        else:
            post.type = "A"
        print(self.request.path.split("/"))
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')