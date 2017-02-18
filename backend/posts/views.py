

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify

from comments.utils import get_comment_list


from .models import Post
from .forms import PostForm
from core.utils import rank_hot
from tags.models import Tag
from categories.models import Category
from comments.models import Comment

class FilterMixin(object):
    paginate_by = 15
    def get_queryset(self):
        qs = super(FilterMixin, self).get_queryset()

        # Filtering by type, level, price, category

        posttype = self.request.GET.get('posttype')
        if posttype:
            qs = qs.filter(post_type=posttype)   

        level = self.request.GET.get('level')
        if level:
            qs = qs.filter(post_level=level)   

        price = self.request.GET.get('price')       
        if price:
            qs = qs.filter(post_price=price)

        category = self.request.GET.get('category')
        if category:
            category = Category.objects.get(slug=category)
            qs = qs.filter(category=category)            

        # Filter by query.
        query = self.request.GET.get('query')
        if query:
            # Search in titles, descriptions, authors, tags
            qs = qs.filter(Q(title__icontains=query) |
                           Q(body__icontains=query) |
                           Q(author__username__icontains=query) |
                           Q(tags__title__icontains=query))                    




        # Sort
        # (Turns queryset into the list, can't just .filter() later
        # sorting = self.request.GET.get('sorting')
        # if sorting == 'top':
        #     qs = qs.order_by('-score')
        # elif sorting == 'new':
        #     qs = qs.order_by('-pub_date')
        # else:
        #     qs = rank_hot(qs)
        qs = qs.order_by('-score', '-pub_date')
        
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

        # All Categories
        categories = Category.objects.all()        
        context['categories'] = categories

        # Solo Tag
        context['tag'] = self.request.GET.get('tag')


        # Pass selected filters (to show them in subnav).
        posttype = self.request.GET.get('posttype')
        if posttype:
            context['posttype'] = posttype.title()
        level = self.request.GET.get('level')
        if level:
            context['level'] = level.title()
        price = self.request.GET.get('price')       
        if price:
            context['price'] = price.title()

        category = self.request.GET.get('category')
        if category:
            category = Category.objects.get(slug=category)
            context['category'] = category.title

            
        # Query
        query = self.request.GET.get('query')
        if query:
            context['query'] = query
            urlstring += "&query=" + query            

        context['urlstring'] = urlstring

        context['submitform'] = PostForm()
        
        return context
    


class BrowseView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"



class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'    
    template_name = "posts/post-detail.html"


    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['submitform'] = PostForm()
        categories = Category.objects.all()        
        context['categories'] = categories

        # Comments
        top_lvl_comments =Comment.objects.filter(post=self.object, parent = None)
        ranked_comments = top_lvl_comments.order_by('score', '-pub_date')
        nested_comments = list(get_comment_list(ranked_comments, rankby="hot"))
        context['comments'] = nested_comments

        return context
    

def post_edit(request, slug):
    post = Post.objects.get(slug=slug)
    # throw him out if he's not an author
    if request.user != post.author and not request.user.is_staff:
        return HttpResponseRedirect('/')        

    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()                

            # Replace tags
            tags = request.POST.get('tags')
            post.tags.set([])
            if tags:
                tags = tags.split(",")
                for tag in tags:
                    title = tag.strip()
                    slug = slugify(title)
                    # Get tag by slug. Create tag if it doesn't exist.
                    try: 
                        tag = Tag.objects.get(slug=slug)
                    except:
                        tag = Tag.objects.create(title=tag)
                    post.tags.add(tag)

            # Set category
            category = request.POST.get('post_category')
            if category:
                category = Category.objects.get(slug=category)
                post.category = category
            post.save()

            
            return HttpResponseRedirect('/post/'+post.slug+'/')
    else:
        form = PostForm(instance=post)
        post_tags = [tag.title for tag in post.tags.all()]
        post_tags = ",".join(post_tags)
        # form.fields["tags"] = []

    return render(request, 'posts/edit.html', {
        'post':post,
        'form':form,
        'post_tags':post_tags,
        'categories': Category.objects.all(),
    })
    

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    context_object_name = 'post'    
    template_name = "posts/edit.html"

    # def form_valid(self,form):
    #     clean = form.cleaned_data
        
    #     # Add tags
    #     tags = request.POST.get('tags')
    #     if tags:
    #         tags = tags.split(",")
    #         for tag in tags:
    #             title = tag.strip()
    #             slug = slugify(title)
    #             # Get tag by slug. Create tag if it doesn't exist.
    #             try: 
    #                 tag = Tag.objects.get(slug=slug)
    #             except:
    #                 tag = Tag.objects.create(title=tag)
    #             post.tags.add(tag)

    #     # Add category
    #     category = request.POST.get('post_category')
    #     if category:
    #         category = Category.objects.get(slug=category)
    #         post.category = category
    #     post.save()

    
    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['submitform'] = PostForm(instance=self.object)
        categories = Category.objects.all()        
        context['categories'] = categories

        return context

def post_delete(request, slug):
    post = Post.objects.get(slug=slug)

    # throw him out if he's not an author
    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.delete()
    return HttpResponseRedirect('/') 
    


class TagView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(TagView, self).get_queryset()

        # Filter by tag
        tag = Tag.objects.get(slug=self.kwargs['slug'])
        # qs = [p for p in qs if (tag in p.tags.all())]
        posts = []
        for post in qs:
            for t in post.tags.all():
                if t.slug==tag.slug:
                    posts.append(post)
        qs = posts
        return qs
        
    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag = Tag.objects.get(slug=self.kwargs['slug'])
        context['tagtitle'] = tag.title
        context['tag'] = tag
        return context    
    


# Voting
def upvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score += 1
    post.save()
    post.author.karma += 1
    post.author.save()
    user = request.user
    user.upvoted.add(post)
    user.save()
    return HttpResponse()

def unupvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score -= 1
    post.save()
    post.author.karma -= 1
    post.author.save()
    user = request.user
    user.upvoted.remove(post)
    user.save()
    return HttpResponse()

    



def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.score += 1 # self upvote
            post.save()

            # request.user.upvoted.add(post)

            # Add tags
            tags = request.POST.get('tags')
            if tags:
                tags = tags.split(",")
                for tag in tags:
                    title = tag.strip()
                    slug = slugify(title)
                    # Get tag by slug. Create tag if it doesn't exist.
                    try: 
                        tag = Tag.objects.get(slug=slug)
                    except:
                        tag = Tag.objects.create(title=tag)
                    post.tags.add(tag)

            # Add category
            category = request.POST.get('post_category')
            if category:
                category = Category.objects.get(slug=category)
                post.category = category
            post.save()

            
                    
            # post.hubs.add(*form.cleaned_data['tags'])
            # hubs = post.hubs.all()
            
            return HttpResponseRedirect('/post/'+post.slug)

    else:
        # for errors
        return render(request, 'posts/create.html', {
            'submitform':form,
        })
