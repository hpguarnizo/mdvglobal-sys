from cities_light.models import Country
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from home.forms import LoginForm
from tienda.emails import email_productos
from tienda.forms import NuevoProducto, NuevaCategoria, EditarProducto, CompraForm, CompletarCompra, EnviarCompraForm
from tienda.models import Producto, TipoProducto, CategoriaProducto, Compra, DetalleCompra


def BuscarProductos(request):
    query = request.GET.get("q", "")
    orden = request.GET.get("orden", "1")
    tipo = request.GET.get("tipo", "")
    categoria = request.GET.get("categoria", "")
    comienzo = request.GET.get("comienzo", "")
    if comienzo and int(comienzo) > 0:
        comienzo = int(comienzo)
    else:
        comienzo = 0

    if orden=="":
        orden = 1
    else:
        orden = int(orden)
        if orden < 1 or orden > 4:
            orden=1

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

    orden_dic={
        1:"-cantidad_vendidos",
        2:"-precio",
        3:"precio",
        4:"-descuento",
    }
    productos = Producto.objects.order_by(orden_dic[orden]).filter(qset).distinct()
    results = productos[comienzo:comienzo+9]
    if len(results)==0 and comienzo>8:
        comienzo = comienzo - 9
        results = productos[comienzo:comienzo + 9]
    pagina = int((comienzo+9)/9)
    return render(request, 'tienda_producto_buscar.html',
                  {'tipos': TipoProducto.objects.all(), 'categorias': CategoriaProducto.objects.all(),
                   'productos': results,"q":query,"tipo_q":tipo,"categoria_q":categoria,"comienzo":comienzo,
                   "cantidad":len(productos), "pagina":pagina,"orden":orden})

def TodosProductos(request):
    comienzo = request.GET.get("comienzo","")
    if comienzo:
        productos = Producto.objects.all().order_by("-fecha")[comienzo:8]
    else:
        productos = Producto.objects.all().order_by("-fecha")[:8]


    return render(request,'tienda_productos.html',{'tipos':TipoProducto.objects.all().order_by("nombre"),'categorias':CategoriaProducto.objects.all(),
                                                  'productos': productos,
                                                   'mayores_ofertas':Producto.objects.all().order_by("-descuento")[:3],
                                                   'mas_buscados':Producto.objects.all().order_by("-precio")[:3],
                                                   'mas_vendidos':Producto.objects.all().order_by("-cantidad_vendidos")[:3]})


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
                               'imagen':producto.get_imagen(),'imagen2':producto.get_imagen2(),'imagen3':producto.get_imagen3(),
                               'descuento':producto.get_descuento()})
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
    comienzo = request.GET.get("comienzo","")
    query = request.GET.get("q","")
    if comienzo and int(comienzo) > 0:
        comienzo = int(comienzo)
    else:
        comienzo = 0
    if query:
        qset = (
            Q(nombre__icontains=query) |
            Q(email__icontains=query) |
            Q(user__email__icontains=query) |
            Q(user__provincia__name__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(provincia__name__icontains=query) |
            Q(provincia__country__name__icontains=query) |
            Q(ciudad__name__icontains=query) |
            Q(estado__nombre__icontains=query)
        )
        compras = Compra.objects.filter(qset).order_by("-fecha").distinct()[comienzo:comienzo+20]
        if len(compras)==0:
            comienzo = comienzo-20
            compras = Compra.objects.filter(qset).order_by("-fecha").distinct()[comienzo:comienzo + 20]

    else:
        compras = Compra.objects.all()[comienzo:comienzo+20]
        if len(compras)==0 and Compra.objects.all().exists():
            comienzo = comienzo-20
            compras = Compra.objects.all()[comienzo:comienzo + 20]

    return render(request,'tienda_ventas.html',{"ventas":compras,"q":query,"comienzo":comienzo})


def VerDetalle(request,compra_id):
    compra = get_object_or_404(Compra,id=compra_id)
    return render(request,'tienda_detalle.html',{"compra":compra})


def EnviarCompra(request,compra_id):
    compra = get_object_or_404(Compra,id=compra_id)
    if request.method=="POST":
        form = EnviarCompraForm(request.POST)
        if form.is_valid():
            compra.enviar(form.cleaned_data["codigo"],form.cleaned_data["url"])
            compra.enviar_email_envio(request)
            return HttpResponseRedirect(reverse('tienda_ventas'))
    else:
        form = EnviarCompraForm()
    return render(request,'tienda_enviar_compra.html',{"form":form,"compra":compra})


def VentasEnvio(request):
    return render(request,'tienda_ventas_enviar.html',{"ventas":Compra.objects.filter(estado=2)})


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


def TiendaLogin(request,producto_id):
    producto = get_object_or_404(Producto,id=producto_id)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(username=email, password=password)

            if user is not None and user.verify_email:
                if not user.is_active:
                    user.set_is_active(True)
                    user.save()
                login(request, user)

                return HttpResponseRedirect(reverse('tienda_agregar_carrito', kwargs={'producto_id':producto_id}))
            else:
                # Return an 'invalid login' error message.
                form.add_error("email", "El email o password son invalidos")
    else:
        form = LoginForm()
    return render(request, 'tienda_registro.html', {'producto': producto, 'form': form})


def TiendaCompletarPerfil(request,producto_id):
    user = request.user
    if request.method == "POST":
        form = CompletarCompra(request.POST)
        if form.is_valid():
            user.set_provincia(form.cleaned_data["provincia"])
            user.set_email(form.cleaned_data["email"])
            compra= form.save(commit=False)
            compra.set_user(user)
            compra.set_direccion(form.cleaned_data["direccion"])
            return HttpResponseRedirect(reverse('tienda_agregar_carrito', kwargs={"producto_id": producto_id}))
    else:
        form = CompletarCompra()
    return render(request, 'tienda_perfil_completar.html', {'form': form})



def TiendaSinRegistro(request,producto_id):

    if request.method=="POST":
        form = CompraForm(request.POST)
        if form.is_valid():
            if not Compra.objects.filter(email=form.cleaned_data["email"],estado=1).exists():
                compra = form.save()
                compra.set_token()
                compra.save()
            else :
                compra= Compra.objects.get(email=form.cleaned_data["email"],estado=1)
            request.session["token_compra"] = compra.get_token()
            return HttpResponseRedirect(reverse('tienda_agregar_carrito', kwargs={"producto_id": producto_id}))
    else:
        form = CompraForm()
    return render(request,'tienda_sin_registro.html',{"form":form,'countrys':Country.objects.all()})



def Carrito(request):
    compra = get_compra(request)
    if compra:
        return render(request, "tienda_carrito.html")
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
        email_productos(request,compra)
        return render(request,'tienda_envio.html',{'compra':compra})
    else:
        raise Http404


def get_compra(request):
    user = request.user
    compra = None
    if user.is_authenticated and Compra.objects.filter(user=user,estado__id=1).exists():
        compra =Compra.objects.get(user=user,estado__id=1)
    elif "token_compra" in request.session:
        token =request.session["token_compra"]
        if Compra.objects.filter(token=token, estado__id=1).exists():
            compra = Compra.objects.get(token=token, estado__id=1)
    else:
        return None
    return compra
