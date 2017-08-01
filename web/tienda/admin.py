from django.contrib import admin
from tienda.models import CategoriaProducto, Compra, DetalleCompra, Producto

admin.site.register(CategoriaProducto)
admin.site.register(Compra)
admin.site.register(Producto)
admin.site.register(DetalleCompra)
