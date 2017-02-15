from django.conf.urls import url
from django.contrib.auth.views import logout

from .views import login, join, email_subscribe

urlpatterns = [
    url(r'^logout/', logout),
    url('^login/$', login),
    url(r'^join/', join),

    # url(r'^preferences/$', views.preferences),
    # url(r'^update-password/$', views.update_password),

    # url(r'^@(?P<username>[^\.]+)', views.profile),

    url(r'^subscribe/', email_subscribe),
    
]
