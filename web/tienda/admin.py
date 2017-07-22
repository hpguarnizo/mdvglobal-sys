from django.contrib import admin
from tienda.models import CategoriaProducto, Compra, DetalleCompra

admin.site.register(CategoriaProducto)
admin.site.register(Compra)
admin.site.register(DetalleCompra)