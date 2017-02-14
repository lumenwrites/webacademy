

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from tags.models import Tag


class FilterMixin(object):
    paginate_by = 15
    def get_queryset(self):
        qs = super(FilterMixin, self).get_queryset()

        # Filter by category
        # try:
        #     selectedhubs = self.request.GET['hubs'].split(",")
        # except:
        #     selectedhubs = []

        # Filter by posttype
        posttype = self.request.GET.get('posttype')
        if posttype:
            qs = qs.filter(post_type=posttype)   
        level = self.request.GET.get('level')
        if level:
            qs = qs.filter(post_level=level)   
        price = self.request.GET.get('price')
        if price:
            qs = qs.filter(post_price=price)   

        # Filter by query
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(Q(title__icontains=query) |
                           Q(body__icontains=query) |
                           Q(author__username__icontains=query))                    




        # Sort
        # (Turns queryset into the list, can't just .filter() later
        # sorting = self.request.GET.get('sorting')
        # if sorting == 'top':
        #     qs = qs.order_by('-score')
        # elif sorting == 'new':
        #     qs = qs.order_by('-pub_date')
        # else:
        #     qs = rank_hot(qs)

        return qs

    def get_context_data(self, **kwargs):
        context = super(FilterMixin, self).get_context_data(**kwargs)
        urlstring = ""
        # Sorting
        # if self.request.GET.get('sorting'):
        #     sorting = self.request.GET.get('sorting')
        # else:
        #     sorting = "hot"
        # context['sorting'] = sorting


        # All Tags
        tags = Tag.objects.all()
        tags = Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')   
        context['tags'] = tags

        # Solo Tag
        context['tag'] = self.request.GET.get('tag')


        # Query
        query = self.request.GET.get('query')
        if query:
            context['query'] = query
            urlstring += "&query=" + query            

        context['urlstring'] = urlstring

        return context
    


class BrowseView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"



class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'    
    template_name = "posts/post-detail.html"
