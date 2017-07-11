from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from contenido.forms import NuevoContenidoForm, NuevaCategoria
from contenido.models import Contenido, CategoriaContenido, TipoContenido


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
    if query:
        qset = (
            Q(nombre__icontains=query) |
            Q(tipo__nombre__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )
        results = Contenido.objects.filter(qset).distinct()
        return render(request, 'contenido.html',
                      {'tipos': TipoContenido.objects.all(), 'categorias': CategoriaContenido.objects.all(),
                       'contenido': results})

    return render(request,'contenido.html',{'tipos':TipoContenido.objects.all(),'categorias':CategoriaContenido.objects.all(),
                                            'contenido':Contenido.objects.all().order_by("-fecha")[:10]})


def ContenidoVerMas(request, contenido_id):
    contenido = get_object_or_404(Contenido, id=contenido_id)
    return render(request,'contenido_ver_mas.html',{'contenido':contenido,'permitido':contenido.puede_verlo(request.user)})
