from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.BrowseView.as_view()),
    url(r'^post/(?P<slug>[^\.]+)/$',
        views.PostDetailView.as_view(),
        name='post-detail'),
]
