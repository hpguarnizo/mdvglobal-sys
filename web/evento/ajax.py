from cities_light.models import City, Region
from django.http import JsonResponse

from evento.models import Evento, Entrada


def get_regions(request):
    country_id = request.GET.get("id_country","")
    response={}
    options = "<option value='' selected='selected'>---------</option>"
    if country_id:
        for region in Region.objects.filter(country_id=country_id):
            options += '<option value="%i">%s</option>'%(region.pk,region.name)
    response["regions"] = options

    return JsonResponse(response)

def get_cities(request):
    region_id = request.GET.get("id_region","")
    response={}
    options = "<option value='' selected='selected'>---------</option>"
    if region_id:
        for city in City.objects.filter(region_id=region_id):
            options += '<option value="%s">%s</option>'%(city.pk,city.name)

    response["cities"] = options

    return JsonResponse(response)

def borrar_evento(request):
    id = request.GET.get("evento_id","")
    evento = Evento.objects.get(id=id)
    response={}
    if not evento.get_tipo().es_pago() or (evento.get_tipo().es_pago() and evento.get_asistentes()==0):
        evento.delete()
        response["borrado"] = "true"
    else:
        response["borrado"] = "false"

    return JsonResponse(response)


def asistir_entrada(request):
    entrada_id = request.GET.get("entrada_id","")
    entrada = Entrada.objects.get(id=entrada_id)
    entrada.asistir()
    response ={}
    response["asistio"] = "true"
    return JsonResponse(response)