from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from accounts.models import _generate_code
from blog.emails import email_verify_suscriptor
from blog.models import Subscriber, CodeValidatorBlog
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

def Suscribirse(request):
    email = request.GET.get("email","")
    suscripto = "false"

    if email:
        aux_subscriber = Subscriber.objects.filter(email=email)
        if len(aux_subscriber) == 0:
            suscriber = Subscriber(email=email)
            suscriber.save()
        else:
            subscriber = aux_subscriber[0]
            if not subscriber.confirmed and not subscriber.subscribe_email:
                subscriber.subscribe_email = True
                subscriber.save()
                code = CodeValidatorBlog.objects.filter(subscriber=subscriber)
                code.delete()

        code = CodeValidatorBlog(code=_generate_code(), subscriber=subscriber)
        code.save()

        email_verify_suscriptor(request,code, subscriber)
        suscripto = "true"

    response={}
    response["suscripto"] = suscripto

    return JsonResponse(response)