from django.conf.urls import url
from evento.ajax import get_regions, get_cities, borrar_evento, asistir_entrada
from evento.views import *

urlpatterns =[
    url(r'entradas/$',EventoEntradas, name='evento_entradas'),
    url(r'lista/$',ListaEventos, name='evento_lista'),
    url(r'transmitir/(?P<evento_id>(\d*))/$',Transmitir, name='evento_transmitir'),
    url(r'seleccionar/(?P<evento_id>(\d*))/$',EventoSeleccionado, name='evento_seleccionar'),
    url(r'completar/perfil/(?P<evento_id>(\d*))/$',CompletarPerfil, name='evento_completar_perfil'),
    url(r'sin/registro/(?P<evento_id>(\d*))/$',EntradaSinRegistro, name='evento_sin_registro'),
    url(r'registro/(?P<evento_id>(\d*))/$',EventoRegistro, name='evento_registro'),
    url(r'comprado/(?P<entrada_id>(\d*))/$',EventoComprado, name='evento_comprado'),
    url(r'todos/$',TodosEventos, name='evento_todos'),
    url(r'nuevo/$',NuevoEvento, name='evento_nuevo'),
    url(r'editar/$',EditarEvento, name='evento_editar'),
    url(r'get_regions/$',get_regions, name='get_regions'),
    url(r'get_cities/$',get_cities, name='get_cities'),
    url(r'asistir_entradas/$',asistir_entrada, name='asistir_entrada'),
    url(r'borrar_evento/$',borrar_evento, name='evento_borrar'),

]