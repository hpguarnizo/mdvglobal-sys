from cities_light.models import Country, City
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from evento.emails import email_evento_nuevo, email_entrada_nueva
from evento.forms import FormEvento, FormEventoEdit, PerfilCompletar, EntradaForm
from evento.models import Evento, Disponible, Entrada, Pagada
from home.forms import LoginForm
from tienda.models import Producto


def ListaEventos(request):
    eventos = Evento.objects.filter(estado__in=[1,2]).order_by('fecha')
    return render(request,'evento_lista.html',{'eventos':eventos})


def EventoSeleccionado(request,evento_id):
    return render(request,'evento_seleccionar.html',{'evento':Evento.objects.get(id=evento_id)})


def TodosEventos(request):
    eventos = Evento.objects.all().order_by('fecha')
    return render(request,'evento_todos.html',{'eventos':eventos})


def EventosSeleccionar(request):
    eventos = Evento.objects.filter(estado=Disponible.objects.all().first()).order_by('fecha')
    return render(request,'evento_seleccionar.html',{'eventos':eventos})


def NuevoEvento(request):
    if request.method =='POST':
        form = FormEvento(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            if evento.es_fecha_valida():
                if evento.es_precio_valido():
                    evento.save()
                    email_evento_nuevo(evento)
                    return HttpResponseRedirect(reverse('evento_todos'))
                else:
                    form.add_error("precio", "El precio debe ser positivo")
            else:
                form.add_error("fecha","La fecha debe ser mayor al dia de hoy")
    else:
        form = FormEvento()
    return render(request,'evento_nuevo.html',{'form':form,'countrys':Country.objects.all()})


def EditarEvento(request):
    id = request.GET.get("evento_id","")
    evento = get_object_or_404(Evento,id=id)

    if request.method =='POST':
        form = FormEventoEdit(request.POST)
        if form.is_valid():
            evento.set_data(form.cleaned_data["nombre"],form.cleaned_data["descripcion"],form.cleaned_data["cupo"],
                            form.cleaned_data["precio"],form.cleaned_data["direccion"],form.cleaned_data["imagen"])
            evento.save()
            return HttpResponseRedirect(reverse('evento_todos'))
    else:
        form = FormEventoEdit(instance=evento)
    return render(request,'evento_editar.html',{'form':form,"evento":evento})

def EventoRegistro(request,evento_id):
    user = request.user
    evento = get_object_or_404(Evento, id=evento_id)

    if user.is_authenticated:
        if not Entrada.objects.filter(evento=evento,user=user).exists():
            if evento.get_tipo().es_pago():
                entrada = Entrada(user=user,evento=evento)
            else:
                entrada = Entrada(user=user,estado=Pagada.objects.all().first(),evento=evento)
            entrada.set_evento(evento)
            entrada.save()
            entrada.set_codigo()
            entrada.save()
            email_entrada_nueva(entrada)

            if evento.get_tipo().es_pago():
                return HttpResponseRedirect(reverse('pay_entrada', kwargs={"entrada_id": entrada.id}))

        else:
            entrada = Entrada.objects.get(evento=evento, user=user)
        return HttpResponseRedirect(reverse('evento_comprado',kwargs={"entrada_id":entrada.id}))

    if request.method=="POST":
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

                return HttpResponseRedirect(reverse('evento_registro'))
            else:
                # Return an 'invalid login' error message.
                form.add_error("email","El email o password son invalidos")
    else:
        form = LoginForm()
    return render(request,'evento_registro.html',{'evento':evento,'form':form})


def EventoComprado(request,entrada_id):
    entrada = get_object_or_404(Entrada,id=entrada_id)
    return render(request,'evento_comprado.html',{'entrada':entrada})


def EntradaSinRegistro(request,evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method=="POST":
        form = EntradaForm(request.POST)
        if form.is_valid():
            if not Entrada.objects.filter(email=form.cleaned_data["email"],evento=evento).exists():
                entrada = form.save()
                entrada.set_evento(evento)
                entrada.save()
                entrada.set_codigo()
                entrada.save()
            else :
                entrada = Entrada.objects.get(email=form.cleaned_data["email"],evento=evento)

            email_entrada_nueva(entrada)
            if evento.get_tipo().es_pago() and entrada.get_estado().es_sin_pagar():
                return HttpResponseRedirect(reverse('pay_entrada', kwargs={"entrada_id": entrada.id}))
            else:
                entrada.pagar(entrada)
                return HttpResponseRedirect(reverse('evento_comprado', kwargs={"entrada_id": entrada.id}))

    else:
        form = EntradaForm()
    return render(request,'evento_sin_registro.html',{"form":form,'countrys':Country.objects.all()})


def CompletarPerfil(request,entrada_id):
    entrada = get_object_or_404(Entrada,id=entrada_id)
    user = request.user
    if request.method=="POST":
        form = PerfilCompletar(request.POST)
        if form.is_valid():
            user.set_provincia(form.cleaned_data["provincia"])
            user.set_email(form.cleaned_data["email"])

            return HttpResponseRedirect(reverse('evento_resgitro', kwargs={"evento_id": entrada.get_evento().id}))
    else:
        form = PerfilCompletar()
    return render(request,'evento_completar_perfil.html',{'form':form})
