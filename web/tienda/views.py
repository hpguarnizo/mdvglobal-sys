from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from tienda.forms import NuevoProducto, NuevaCategoria, EditarProducto
from tienda.models import Producto, TipoProducto, CategoriaProducto, Compra


def TodosProductos(request):
    query = request.GET.get("q", "")
    if query:
        qset = (
            Q(nombre__icontains=query) |
            Q(tipo__nombre__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )
        results = Producto.objects.filter(qset).distinct()
        return render(request, 'tienda_productos.html',
                      {'tipos': TipoProducto.objects.all(), 'categorias': CategoriaProducto.objects.all(),
                       'productos': results})

    return render(request,'tienda_productos.html',{'tipos':TipoProducto.objects.all(),'categorias':CategoriaProducto.objects.all(),
                                                  'productos':Producto.objects.all().order_by("-fecha")[:10]})


def ListaProductos(request):
    return render(request,'tienda_lista_productos.html',{'productos':Producto.objects.filter(eliminado=False)})


def ProductoNuevo(request):
    if request.method == "POST":
        form = NuevoProducto(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tienda_productos_lista'))
    else:
        form = NuevoProducto()
    return render(request,'tienda_productos_nuevo.html',{'form':form})


def ProductoEditar(request):
    producto = get_object_or_404(Producto,id=request.GET.get("producto_id",""))
    if request.method == "POST":
        form = EditarProducto(request.POST)
        if form.is_valid():
            producto.set_data(form.save(commit=False))
            producto.save()
            return HttpResponseRedirect(reverse('tienda_productos_lista'))
    else:
        form = EditarProducto({'nombre':producto.get_nombre(),'descripcion':producto.get_descripcion(),
                               'categoria':producto.get_categoria().id,'precio':producto.get_precio(),'stock':producto.get_stock(),
                               'imagen':producto.get_imagen()})
    return render(request,'tienda_productos_editar.html',{'form':form,'producto':producto})


def ListaCategorias(request):
    return render(request,'tienda_categoria_lista.html',{'tipos':TipoProducto.objects.all(),'categorias':CategoriaProducto.objects.all()})


def CategoriaNueva(request):
    if request.method == "POST":
        form = NuevaCategoria(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tienda_categoria_lista'))
    else:
        form = NuevaCategoria()
    return render(request,'tienda_categoria_nuevo.html',{'form':form})

def CategoriaEditar(request):
    categoria = get_object_or_404(CategoriaProducto,id=request.GET.get("categoria_id",""))
    if request.method == "POST":
        form = NuevaCategoria(request.POST)
        if form.is_valid():
            categoria.set_nombre(form.cleaned_data["nombre"])
            categoria.save()
            return HttpResponseRedirect(reverse('tienda_categoria_lista'))
    else:
        form = NuevaCategoria(instance=categoria)
    return render(request,'tienda_categoria_editar.html',{'form':form,'categoria':categoria})


def ListaVentas(request):
    return render(request,'tienda_ventas.html')


def VentasEnvio(request):
    return render(request,'tienda_ventas_enviar.html')


def ProductoVerMas(request,producto_id):
    producto = get_object_or_404(Producto,id=producto_id)
    return render(request,'tienda_ver_mas.html',{"producto":producto})


def AgregarCarrito(request,producto_id):
    producto = get_object_or_404(Producto,producto_id)
    user = request.user
    if user.is_autheticated:
        if Compra.objects.filter(user=user).exists():
            compra =Compra.objects.get(user=user)
        else:
            compra = Compra(user=user)
            compra.save()

        compra.agregar_producto(producto)

