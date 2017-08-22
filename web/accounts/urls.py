from django.conf.urls import  url
from django.contrib.admin.views.decorators import staff_member_required
from accounts.views import PerfilView, DeleteUser

urlpatterns = [
    url(r'^profile/$', staff_member_required(PerfilView), name='profile'),
    url(r'^delete/user/$', staff_member_required(DeleteUser), name='delete_user'),

]


