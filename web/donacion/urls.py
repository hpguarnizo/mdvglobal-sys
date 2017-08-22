from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from donacion.views import *

urlpatterns = [
    url(r'ver/$',staff_member_required(VerDonaciones),name='donacion_ver'),
    url(r'configuracion/$',staff_member_required(Configurar),name='donacion_configuracion'),
    url(r'gracias/(?P<donacion_id>(\d*))/$',DonacionGracias,name='donacion_gracias'),
    url(r'mas/$',DonacionVista,name='donacion_mas'),
]