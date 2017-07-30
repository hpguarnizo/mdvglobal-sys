from django.conf.urls import url

from donacion.views import *

urlpatterns = [
    url(r'ver/$',VerDonaciones,name='donacion_ver'),
    url(r'configuracion/$',Configurar,name='donacion_configuracion'),
    url(r'gracias/(?P<donacion_id>(\d*))/$',DonacionGracias,name='donacion_gracias'),
    url(r'mas/$',DonacionVista,name='donacion_mas'),
]