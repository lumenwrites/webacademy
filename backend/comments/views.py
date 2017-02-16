from django.shortcuts import render
from django.http import HttpResponseRedirect

from posts.models import Post
from .models import Comment
from .forms import CommentForm

def comment_submit(request, post_slug=""):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            if post_slug:
                post = Post.objects.get(slug=post_slug)
                comment.post = post
            comment.save()

            return HttpResponseRedirect(post.get_absolute_url())
        else:
            # If error
            prev_url = request.GET.get('next', '/')
            return HttpResponseRedirect(prev_url)
    else:
        # If not post
        prev_url = request.GET.get('next', '/')
        return HttpResponseRedirect(prev_url)



def reply_submit(request, post_slug, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(slug=post_slug)            
            comment.parent = Comment.objects.get(id=comment_id)
            comment.save()

            # comment_url = request.GET.get('next', '/')+"#id-"+str(comment.id)
            return HttpResponseRedirect(comment.post.get_absolute_url())
        else:
            comment_url = request.GET.get('next', '/')
            return HttpResponseRedirect(comment_url)
    return HttpResponseRedirect('/error')                    
    
