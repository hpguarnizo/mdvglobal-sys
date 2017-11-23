from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from evento.ajax import get_regions, get_cities, borrar_evento, asistir_entrada, enviar_emails
from evento.views import *

urlpatterns =[
    url(r'entradas/$',staff_member_required(EventoEntradas), name='evento_entradas'),
    url(r'lista/$',ListaEventos, name='evento_lista'),
    url(r'en/vivo/$',TransmisionEnVivo, name='evento_en_vivo'),
    url(r'convocatoria/(?P<evento_id>(\d*))/$',Convocatoria, name='evento_convocatoria'),
    url(r'transmitir/(?P<evento_id>(\d*))/$',staff_member_required(Transmitir), name='evento_transmitir'),
    url(r'seleccionar/(?P<evento_id>(\d*))/$',EventoSeleccionado, name='evento_seleccionar'),
    url(r'completar/perfil/(?P<evento_id>(\d*))/$',CompletarPerfil, name='evento_completar_perfil'),
    url(r'sin/registro/(?P<evento_id>(\d*))/$',EntradaSinRegistro, name='evento_sin_registro'),
    url(r'registro/(?P<evento_id>(\d*))/$',EventoRegistro, name='evento_registro'),
    url(r'comprado/(?P<entrada_id>(\d*))/$',EventoComprado, name='evento_comprado'),
    url(r'todos/$',staff_member_required(TodosEventos), name='evento_todos'),
    url(r'nuevo/$',staff_member_required(NuevoEvento), name='evento_nuevo'),
    url(r'editar/$',staff_member_required(EditarEvento), name='evento_editar'),
    url(r'get_regions/$',get_regions, name='get_regions'),
    url(r'get_cities/$',get_cities, name='get_cities'),
    url(r'asistir_entradas/$',staff_member_required(asistir_entrada), name='asistir_entrada'),
    url(r'borrar_evento/$',staff_member_required(borrar_evento), name='evento_borrar'),
    url(r'enviar_emails/$',staff_member_required(enviar_emails), name='enviar_emails'),

]