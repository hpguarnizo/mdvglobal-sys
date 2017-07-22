from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from tienda.forms import NuevoProducto, NuevaCategoria, EditarProducto
from tienda.models import Producto, TipoProducto, CategoriaProducto, Compra, DetalleCompra


def BuscarProductos(request):
    query = request.GET.get("q", "")
    tipo = request.GET.get("tipo", "")
    categoria = request.GET.get("categoria", "")
    comienzo = request.GET.get("comienzo", "")
    if comienzo and int(comienzo) > 0:
        comienzo = int(comienzo)
    else:
        comienzo = 0
    if query or tipo or categoria:
        if query and tipo and categoria:
            qset = (
                Q(nombre__icontains=query) &
                Q(tipo__nombre__exact=tipo) &
                Q(categoria__nombre__exact=categoria)
            )
        elif query and tipo:
            qset = (
                Q(nombre__icontains=query) &
                Q(tipo__nombre__exact=tipo)
            )
        elif query and categoria:
            qset = (
                Q(nombre__icontains=query) &
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
    else:
        return HttpResponseRedirect(reverse('tienda_productos'))

    productos = Producto.objects.filter(qset).distinct()
    results = productos[comienzo:comienzo+10]
    return render(request, 'tienda_producto_buscar.html',
                  {'tipos': TipoProducto.objects.all(), 'categorias': CategoriaProducto.objects.all(),
                   'productos': results,"q":query,"tipo_q":tipo,"categoria_q":categoria,"comienzo":comienzo,
                   "cantidad":len(productos)})

def TodosProductos(request):
    comienzo = request.GET.get("comienzo","")
    if comienzo:
        productos = Producto.objects.all().order_by("-fecha")[comienzo:8]
    else:
        productos = Producto.objects.all().order_by("-fecha")[:8]


    return render(request,'tienda_productos.html',{'tipos':TipoProducto.objects.all(),'categorias':CategoriaProducto.objects.all(),
                                                  'productos': productos,
                                                   'mayores_ofertas':Producto.objects.all().order_by("descuento")[:3],
                                                   'mas_baratos':Producto.objects.all().order_by("-precio")[:3],
                                                   'mas_vendidos':Producto.objects.all().order_by("cantidad_vendidos")[:3],
                                                   'compra':get_compra(request)})


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
    sin_stock = request.GET.get("sin_stock","")
    tipos = TipoProducto.objects.all()
    return render(request,'tienda_ver_mas.html',{"producto":producto,"tipos":tipos,
                                                 "productos_que_gustan":Producto.objects.all().order_by("?")[:6],
                                                 "sin_stock":sin_stock})


def AgregarCarrito(request,producto_id):
    producto = get_object_or_404(Producto,id=producto_id)
    cantidad = int(request.GET.get("cantidad","1"))
    if not producto.hay_stock(cantidad):
        return HttpResponseRedirect(reverse("producto_ver_mas",kwargs={"producto_id":producto_id})+"?sin_stock=True")
    user = request.user
    if user.is_authenticated:
        if Compra.objects.filter(user=user, estado=1).exists():
            compra =Compra.objects.get(user=user, estado=1)
        else:
            compra = Compra(user=user)
            compra.save()

        compra.agregar_producto(producto,cantidad)
        return HttpResponseRedirect(reverse("tienda_carrito"))

    elif "token_compra" in request.session:
        token =request.session["token_compra"]
        compra = Compra.objects.get(token=token)
        compra.agregar_producto(producto,cantidad)
        return HttpResponseRedirect(reverse("tienda_carrito"))

    else:
        return HttpResponseRedirect(reverse('tienda_login_producto',kwargs={"producto_id":producto_id}))

def Carrito(request):
    compra = get_compra(request)
    if compra:
        return render(request, "tienda_carrito.html", {"compra": compra})
    else:
        return HttpResponseRedirect(reverse('tienda_productos'))


def EliminarDetalle(request,detalle_id):
    detalle= DetalleCompra.objects.get(id=detalle_id)
    if detalle.get_compra().get_estado().es_incompleta():
        compra = detalle.get_compra()
        compra.set_total(compra.get_total()-(detalle.get_producto().get_precio()*detalle.get_cantidad()))
        compra.save()
        detalle.delete()

    if compra.get_detalle():
        return HttpResponseRedirect(reverse('tienda_carrito'))
    else:
        return HttpResponseRedirect(reverse('tienda_productos'))


def MenosDetalle(request,detalle_id):
    detalle = DetalleCompra.objects.get(id=detalle_id)
    if detalle.get_compra().get_estado().es_incompleta():
        detalle.quitar()
        detalle.save()
    return HttpResponseRedirect(reverse('tienda_carrito'))

def MasDetalle(request,detalle_id):
    detalle = DetalleCompra.objects.get(id=detalle_id)
    if detalle.get_compra().get_estado().es_incompleta():
        detalle.agregar()
        detalle.save()
    return HttpResponseRedirect(reverse('tienda_carrito'))

def EnvioProductos(request,compra_id):
    compra = get_object_or_404(Compra,id=compra_id)
    if not compra.get_estado().es_incompleta():

        return render(request,'tienda_envio.html',{'compra':compra})
    else:
        raise Http404


def get_compra(request):
    user = request.user
    if user.is_authenticated and Compra.objects.filter(user=user,estado=1).exists():
        compra =Compra.objects.get(user=user,estado=1)
    elif "token_compra" in request.session:
        token =request.session["token_compra"]
        compra = Compra.objects.get(token=token)
    else:
        return None
    return compra
