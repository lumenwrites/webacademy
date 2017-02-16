from django.conf.urls import url

from .views import comment_submit

urlpatterns = [
    # Comments
    url(r'^comment-submit/(?P<post_slug>[^\.]+)', comment_submit),
    # url(r'^reply-submit/(?P<comment_id>[^\.]+)', reply_submit),

    # url(r'^comment/(?P<comment_id>[^\.]+)/edit', comment_edit),
    # url(r'^comment/(?P<comment_id>[^\.]+)/delete', comment_delete), 

    # url(r'^comment-upvote/', comment_upvote),
    # url(r'^comment-unupvote/', comment_unupvote),
]
