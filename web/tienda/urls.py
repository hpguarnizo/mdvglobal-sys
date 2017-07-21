from django.conf.urls import url

from tienda.ajax import *
from tienda.views import *

urlpatterns = [
    url(r'carrito/menos/$', MenosDetalle, name='tienda_menos_detalle'),
    url(r'carrito/mas/$', MasDetalle, name='tienda_mas_detalle'),
    url(r'carrito/eliminar/$', EliminarDetalle, name='tienda_eliminar_detalle'),
    url(r'carrito/$', Carrito, name='tienda_carrito'),
    url(r'agregar/carrito/(?P<producto_id>(\d*))/$', AgregarCarrito, name='tienda_agregar_carrito'),
    url(r'productos/buscar/$', BuscarProductos, name='tienda_productos_busqueda'),
    url(r'productos/$',TodosProductos,name='tienda_productos'),
    url(r'productos/lista/$',ListaProductos,name='tienda_productos_lista'),
    url(r'producto/ver/mas/(?P<producto_id>(\d*))/$',ProductoVerMas,name='producto_ver_mas'),
    url(r'producto/nuevo/$',ProductoNuevo,name='tienda_productos_nuevo'),
    url(r'producto/editar/$',ProductoEditar,name='tienda_producto_editar'),
    url(r'producto/borrar/$',producto_borrar,name='producto_borrar'),
    url(r'categoria/lista/$',ListaCategorias,name='tienda_categoria_lista'),
    url(r'categoria/nueva/$',CategoriaNueva,name='tienda_categoria_nuevo'),
    url(r'categoria/editar/$',CategoriaEditar,name='tienda_categoria_editar'),
    url(r'categoria/borrar/$',borrar_categoria,name='categoria_borrar'),
    url(r'ventas/envio/$', VentasEnvio, name='tienda_ventas_envio'),
    url(r'ventas/$',ListaVentas,name='tienda_ventas'),
]