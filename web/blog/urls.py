from django.conf.urls import  url
from blog.views import *

urlpatterns = [

    #url(r'^$', BlogView.as_view(), name='blog'),
    url(r'^verify/email/$', VerifyEmail, name='blog_verify_email'),
    url(r'^unsubscribe/', BlogUnsubscribe, name='blog_unsubscribe'),
]
