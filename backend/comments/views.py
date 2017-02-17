from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

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


# Voting
def comment_upvote(request):
    comment = Comment.objects.get(id=request.POST.get('comment-id'))
    comment.score += 1
    comment.save()
    comment.author.karma += 1
    comment.author.save()
    user = request.user
    user.comments_upvoted.add(comment)
    user.save()
    return HttpResponse()

def comment_unupvote(request):
    comment = Comment.objects.get(id=request.POST.get('comment-id'))
    comment.score -= 1
    comment.save()
    comment.author.karma = 1
    comment.author.save()
    user = request.user
    user.comments_upvoted.remove(comment)
    user.save()
    return HttpResponse()



# class CommentUpdateView(UpdateView):
#     model = Post
#     form_class = PostForm
#     context_object_name = 'post'    
#     template_name = "posts/edit.html"

    
#     def get_context_data(self, **kwargs):
#         context = super(PostUpdateView, self).get_context_data(**kwargs)
#         # context['form'] = PostForm()
#         categories = Category.objects.all()        
#         context['categories'] = categories

#         return context
