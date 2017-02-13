from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.BrowseView.as_view()),    
]
