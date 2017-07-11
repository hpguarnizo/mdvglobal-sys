from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from contenido.models import Contenido, CategoriaContenido


def borrar_contenido(request):
    contenido = get_object_or_404(Contenido,id=request.GET.get("contenido_id","-1"))
    contenido.delete()
    response ={}
    response["borrado"]="true"
    return JsonResponse(response)


def borrar_categoria(request):
    categoria_id = request.GET.get("categoria_id","")
    response={}
    if not Contenido.objects.filter(categoria=categoria_id).exists():
        categoria = get_object_or_404(CategoriaContenido,id=categoria_id)
        categoria.delete()
        response["borrado"] = "true"
    else:
        response["borrado"] = "false"

    return JsonResponse(response)
