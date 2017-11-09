from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from contenido.forms import NuevoContenidoForm, NuevaCategoria
from contenido.models import Contenido, CategoriaContenido, TipoContenido
from tienda.views import get_compra


def ListaContenido(request):
    return render(request,'contenido_lista.html',{'contenidos':Contenido.objects.all()})


def EditarContenido(request):
    contenido = get_object_or_404(Contenido,id=request.GET.get("contenido_id",""))
    if request.method=="POST":
        form = NuevoContenidoForm(request.POST)
        if form.is_valid():
            contenido.set_data(form.save(commit=False))
            contenido.save()
            return HttpResponseRedirect(reverse('contenido_lista'))
    else:
        form = NuevoContenidoForm(instance=contenido)
    return render(request,'contenido_editar.html',{'form':form,'contenido':contenido})


def NuevoContenido(request):
    if request.method=="POST":
        form = NuevoContenidoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contenido_lista'))
    else:
        form = NuevoContenidoForm()
    return render(request,'contenido_nuevo.html',{'form':form})


def CategoriaLista(request):
    return render(request,'contenido_categoria_lista.html',{'tipos':TipoContenido.objects.all(),'categorias':CategoriaContenido.objects.all()})

def CategoriaNueva(request):
    if request.method == "POST":
        form = NuevaCategoria(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contenido_categorias'))
    else:
        form = NuevaCategoria()
    return render(request,'tienda_categoria_nuevo.html',{'form':form})

def CategoriaEditar(request):
    categoria = get_object_or_404(CategoriaContenido,id=request.GET.get("categoria_id",""))
    if request.method == "POST":
        form = NuevaCategoria(request.POST)
        if form.is_valid():
            categoria.set_nombre(form.cleaned_data["nombre"])
            categoria.save()
            return HttpResponseRedirect(reverse('contenido_categorias'))
    else:
        form = NuevaCategoria(instance=categoria)
    return render(request,'tienda_categoria_editar.html',{'form':form,'categoria':categoria})

def ContenidoMostrar(request):
    query = request.GET.get("q", "")
    tipo = request.GET.get("tipo", "")
    categoria = request.GET.get("categoria", "")
    acceso = request.GET.get("acceso", "")
    comienzo = request.GET.get("comienzo", "")
    user = request.user
    if not user.is_anonymous() and user.is_authenticated:
        request.user.finalizo_suscripcion()
    
    if comienzo and int(comienzo)>0:
        comienzo = int(comienzo)
    else:
        comienzo=0
    if query or tipo or categoria or acceso:
        if query and tipo and categoria and acceso:
            qset = (
                Q(nombre__icontains=query) &
                Q(tipo__nombre__exact=tipo) &
                Q(categoria__nombre__exact=categoria) &
                Q(acceso__name__exact=acceso)
            )
        elif tipo and categoria and acceso:
            qset = (
                Q(tipo__nombre__exact=tipo) &
                Q(categoria__nombre__exact=categoria) &
                Q(acceso__name__exact=acceso)
            )
        elif query and tipo and categoria:
            qset = (
                Q(nombre__icontains=query) &
                Q(tipo__nombre__exact=tipo) &
                Q(categoria__nombre__exact=categoria)
            )
        elif query and acceso and categoria:
            qset = (
                Q(nombre__icontains=query) &
                Q(acceso__name__exact=acceso) &
                Q(categoria__nombre__exact=categoria)
            )
        elif query and tipo and acceso:
            qset = (
                Q(nombre__icontains=query) &
                Q(tipo__nombre__exact=tipo) &
                Q(acceso__name__exact=acceso)
            )
        elif query and tipo:
            qset = (
                Q(nombre__icontains=query) &
                Q(tipo__nombre__exact=tipo)
            )
        elif acceso and tipo:
            qset = (
                Q(acceso__name__exact=acceso) &
                Q(tipo__nombre__exact=tipo)
            )
        elif query and acceso:
            qset = (
                Q(nombre__icontains=query) &
                Q(acceso__name__exact=acceso)
            )
        elif query and categoria:
            qset = (
                Q(nombre__icontains=query) &
                Q(categoria__nombre__exact=categoria)
            )
        elif acceso and categoria:
            qset = (
                Q(acceso__name__exact=acceso) &
                Q(categoria__nombre__exact=categoria)
            )
        elif categoria and tipo:
            qset = (
                Q(tipo__nombre__exact=tipo) &
                Q(categoria__nombre__exact=categoria)
            )
        elif query:
            qset = (
                Q(nombre__icontains=query) |
                Q(tipo__nombre__icontains=tipo) |
                Q(categoria__nombre__icontains=categoria)
            )
        elif tipo:
            qset = (
                Q(tipo__nombre__exact=tipo)
            )
        elif categoria:
            qset = (
                Q(categoria__nombre__exact=categoria)
            )
        elif acceso:
            qset = (
                Q(acceso__name__exact=acceso)
            )
        contenidos = Contenido.objects.filter(qset).distinct()
        results = contenidos[comienzo:comienzo+9]
        if len(results)==0:
            comienzo = comienzo-9
            results = contenidos[comienzo:comienzo + 9]
        pagina = int((comienzo+9)/9)
        tipos = TipoContenido.objects.all()
        categorias=CategoriaContenido.objects.all()
        return render(request, 'contenido.html',
                      {'tipos': tipos, 'categorias': categorias,
                       'contenido': results,"q":query,"tipo_q":tipo,"categoria_q":categoria,"comienzo":comienzo,
                       "compra":get_compra(request),"cantidad":len(contenidos),"pagina":pagina,"acceso":acceso})

    contenido = Contenido.objects.all().order_by("-fecha")[comienzo:comienzo+9]
    if len(contenido)==0 and comienzo>=9:
        comienzo-=9
        contenido = Contenido.objects.all().order_by("-fecha")[comienzo:comienzo + 9]
    pagina = int((comienzo+9)/9)
    return render(request,'contenido.html',{'tipos':TipoContenido.objects.all(),
                                            'categorias':CategoriaContenido.objects.all(),
                                            'contenido':contenido,
                                            "compra":get_compra(request),"comienzo":comienzo,"pagina":pagina})


def ContenidoVerMas(request, contenido_id):
    user = request.user
    if not user.is_anonymous() and user.is_authenticated:
        request.user.finalizo_suscripcion()
    contenido = get_object_or_404(Contenido, id=contenido_id)
    return render(request,'contenido_ver_mas.html',{'contenido':contenido,'permitido':contenido.puede_verlo(request.user),
                                                    "compra":get_compra(request)})
