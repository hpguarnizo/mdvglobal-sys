from django.conf.urls import url
from contenido.ajax import borrar_contenido, borrar_categoria
from contenido.views import *

urlpatterns =[
    url(r'ver/mas/(?P<contenido_id>(\d*))/$', ContenidoVerMas, name='contenido_ver_mas'),
    url(r'ver/$',ContenidoMostrar,name='contenido_mostrar'),
    url(r'categoria/nueva/$',CategoriaNueva,name='contenido_categoria_nueva'),
    url(r'categoria/editar/$',CategoriaEditar,name='contenido_categoria_editar'),
    url(r'categoria/borrar/$',borrar_categoria,name='contenido_categoria_borrar'),
    url(r'nuevo/$',NuevoContenido,name='contenido_nuevo'),
    url(r'lista/$',ListaContenido,name='contenido_lista'),
    url(r'editar/$',EditarContenido,name='contenido_editar'),
    url(r'borrar_contenido/$',borrar_contenido,name='contenido_borrar'),
    url(r'categoria/$',CategoriaLista,name='contenido_categorias'),
    ]