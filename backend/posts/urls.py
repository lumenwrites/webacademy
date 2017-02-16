from django.conf.urls import url

from .views import BrowseView, PostDetailView, post_create
from .views import upvote, unupvote

urlpatterns = [
    url(r'^$', BrowseView.as_view()),
    url(r'^post/(?P<slug>[^\.]+)/$', PostDetailView.as_view(), name='post-detail'),
    url(r'^submit$', post_create),

    url(r'^upvote/$', upvote),
    url(r'^unupvote/$', unupvote),
    
]
