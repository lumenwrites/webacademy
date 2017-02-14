from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Post

class BrowseView(ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"


class BrowseView(ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"
    

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'    
    template_name = "posts/post_detail.html"
