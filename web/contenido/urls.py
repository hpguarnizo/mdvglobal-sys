from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from contenido.ajax import borrar_contenido, borrar_categoria
from contenido.views import *

urlpatterns =[
    url(r'ver/mas/(?P<contenido_id>(\d*))/$', ContenidoVerMas, name='contenido_ver_mas'),
    url(r'ver/$',ContenidoMostrar,name='contenido_mostrar'),
    url(r'categoria/nueva/$',staff_member_required(CategoriaNueva),name='contenido_categoria_nueva'),
    url(r'categoria/editar/$',staff_member_required(CategoriaEditar),name='contenido_categoria_editar'),
    url(r'categoria/borrar/$',staff_member_required(borrar_categoria),name='contenido_categoria_borrar'),
    url(r'nuevo/$',staff_member_required(NuevoContenido),name='contenido_nuevo'),
    url(r'lista/$',staff_member_required(ListaContenido),name='contenido_lista'),
    url(r'editar/$',staff_member_required(EditarContenido),name='contenido_editar'),
    url(r'borrar_contenido/$',staff_member_required(borrar_contenido),name='contenido_borrar'),
    url(r'categoria/$',staff_member_required(CategoriaLista),name='contenido_categorias'),
    ]