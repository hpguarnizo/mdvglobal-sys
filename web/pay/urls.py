from django.conf.urls import  url
from pay.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^payment/$', login_required(buy_my_item),name='pay_payment'),
    url(r'^tienda/(?P<compra_id>(\d*))$', buy_my_productos,name='pay_tienda'),
    url(r'^donacion/$', buy_my_donacion,name='pay_donacion'),
    url(r'^ministerial/$', login_required(buy_my_ministerial),name='pay_ministerial'),
    url(r'^premium/$', login_required(buy_my_premium),name='pay_premium'),
    url(r'^entrada/(?P<entrada_id>(\d*))/$', buy_my_entrada,name='pay_entrada'),
    url(r'^return/$', login_required(return_url_premium), name='pay_return_url_premium'),
    url(r'^cancel/$', login_required(cancel_return_premium), name='pay_cancel_return_premium'),
    url(r'^plans/$', HomePayView.as_view(), name='pay_plans'),

]

