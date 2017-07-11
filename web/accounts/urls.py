from django.conf.urls import  url
from accounts.views import PerfilView, DeleteUser
from django.contrib.auth.decorators import login_required



urlpatterns = [
    url(r'^profile/$', login_required(PerfilView), name='profile'),
    url(r'^delete/user/$', login_required(DeleteUser), name='delete_user'),

]


