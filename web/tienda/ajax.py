from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from tienda.models import CategoriaProducto, Producto, DetalleCompra


def borrar_categoria(request):
    categoria_id = request.GET.get("categoria_id","")
    response={}
    if not Producto.objects.filter(categoria=categoria_id).exists():
        categoria = get_object_or_404(CategoriaProducto,id=categoria_id)
        categoria.delete()
        response["borrado"] = "true"
    else:
        response["borrado"] = "false"

    return JsonResponse(response)

def producto_borrar(request):
    producto_id = request.GET.get("producto_id", "")
    producto = Producto.objects.get(id=producto_id)
    producto.eliminar()
    producto.save()
    response={}
    response["borrado"]="true"

    return JsonResponse(response)