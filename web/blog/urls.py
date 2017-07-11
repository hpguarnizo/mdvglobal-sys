from django.conf.urls import  url
from blog.views import *
from django.views.generic import TemplateView

urlpatterns = [

    url(r'^$', BlogView.as_view(), name='blog'),
    url(r'^verify/email/$', VerifyEmail, name='blog_verify_email'),
    url(r'^unsubscribe/', BlogUnsubscribe, name='blog_unsubscribe'),
    url(r'^about/$', AboutView.as_view(), name='blog_about'),
    url(r'^como-atraer-mas-clientes-desde-facebook/$', PostAtraerView, name='blog_post_atraer'),
#    url(r'^ver/', TemplateView.as_view(template_name="blog_confirmed_email.html"), name='blog_unsubscribe'),

]
