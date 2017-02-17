from django.conf.urls import url

from .views import BrowseView, PostDetailView, PostUpdateView, post_create
from .views import upvote, unupvote, post_delete

urlpatterns = [
    url(r'^$', BrowseView.as_view()),
    url(r'^post/(?P<slug>[^\.]+)/edit$', PostUpdateView.as_view()),
    url(r'^post/(?P<slug>[^\.]+)/delete$', post_delete),
    url(r'^post/(?P<slug>[^\.]+)/$', PostDetailView.as_view(), name='post-detail'),

    url(r'^submit$', post_create),

    url(r'^upvote/$', upvote),
    url(r'^unupvote/$', unupvote),
    
]
