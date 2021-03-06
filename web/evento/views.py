from cities_light.models import Country, City
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from evento.emails import email_evento_nuevo, email_entrada_nueva, email_entrada_pago, email_evento_inicia
from evento.forms import FormEvento, FormEventoEdit, PerfilCompletar, EntradaForm, EventoTransmitir
from evento.models import Evento, Disponible, Entrada, Pagada
from home.forms import LoginForm


def EventoEntradas(request):
    evento_id = request.GET.get("evento_id","")
    evento = get_object_or_404(Evento,id=evento_id)
    evento.get_estado().se_termino(evento)
    return render(request,"evento_entradas.html",{"evento":evento})

def ListaEventos(request):
    eventos = Evento.objects.filter(estado__in=[1,2]).order_by('-fecha')
    for evento in eventos:
        evento.get_estado().se_termino(evento)
    return render(request,'evento_lista.html',{'eventos':eventos})


def EventoSeleccionado(request,evento_id):
    evento = Evento.objects.get(id=evento_id)
    evento.get_estado().se_termino(evento)
    return render(request,'evento_seleccionar.html',{'evento':evento})


def TodosEventos(request):
    for evento in Evento.objects.filter(estado_id__in=[1,2]):
        evento.get_estado().se_termino(evento)
    eventos = Evento.objects.all().order_by('-fecha')
    evento_enviar = request.GET.get("eventoenviar")
    return render(request,'evento_todos.html',{'eventos':eventos,'evento_enviar':evento_enviar})


def EventosSeleccionar(request):
    eventos = Evento.objects.filter(estado=Disponible.objects.all().first()).order_by('fecha')
    for evento in eventos:
        evento.get_estado().se_termino(evento)
    return render(request,'evento_seleccionar.html',{'eventos':eventos})


def NuevoEvento(request):
    if request.method =='POST':
        form = FormEvento(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            if evento.es_fecha_valida():
                if evento.es_precio_valido():
                    evento.save()
                    return HttpResponseRedirect(reverse('evento_todos')+"?eventoenviar=%i"%evento.id)
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
                            form.cleaned_data["precio"],form.cleaned_data["direccion"],form.cleaned_data["imagen"],
                            form.cleaned_data["fecha"])
            evento.save()
            return HttpResponseRedirect(reverse('evento_todos'))
    else:
        form = FormEventoEdit(instance=evento)
    return render(request,'evento_editar.html',{'form':form,"evento":evento})

def EventoRegistro(request,evento_id):
    user = request.user
    evento = get_object_or_404(Evento, id=evento_id)

    if user.is_authenticated:
        if not Entrada.objects.filter(evento=evento,user=user,estado__in=[2,3]).exists():
            if evento.get_tipo().es_pago():
                entrada = Entrada(user=user,evento=evento)
            else:
                entrada = Entrada(user=user,estado=Pagada.objects.all().first(),evento=evento)
            entrada.set_evento(evento)
            entrada.save()
            entrada.set_codigo()
            entrada.save()
            evento.get_estado().se_lleno(evento)
            if evento.get_tipo().es_pago():
                email_entrada_pago(request, entrada)
                return HttpResponseRedirect(reverse('pay_entrada', kwargs={"entrada_id": entrada.id}))
            else:
                email_entrada_nueva(request, entrada)

        else:
            entrada = Entrada.objects.get(evento=evento, user=user)
            email_entrada_nueva(request, entrada)

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

            evento.get_estado().se_lleno(evento)

            if evento.get_tipo().es_pago() and entrada.get_estado().es_sin_pagar():
                email_entrada_pago(request,entrada)
                return HttpResponseRedirect(reverse('pay_entrada', kwargs={"entrada_id": entrada.id}))
            else:
                email_entrada_nueva(request, entrada)
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

def Transmitir(request,evento_id):
    evento = get_object_or_404(Evento,id=evento_id)
    if Evento.objects.filter(estado=4).exists():
        evento = Evento.objects.get(estado=4)
        evento.finalizar_transmision()
        return HttpResponseRedirect(reverse("evento_todos"))
    if request.method=="POST":
        form = EventoTransmitir(request.POST)
        if form.is_valid():
            evento.transmitir(form.cleaned_data["url"])
            email_evento_inicia(request,evento)
            return HttpResponseRedirect(reverse('evento_convocatoria',kwargs={"evento_id":evento.id}))
    else:
        form = EventoTransmitir()
    return render(request,'evento_transmitir.html',{'form':form,'evento':evento})

def Convocatoria(request,evento_id):
    evento = get_object_or_404(Evento,id=evento_id)
    evento.get_estado().se_termino(evento)
    return render(request,'evento_convocatoria.html',{"evento":evento})

def TransmisionEnVivo(request):
    if Evento.objects.filter(estado=4):
        evento = Evento.objects.get(estado=4)
        return HttpResponseRedirect(reverse('evento_convocatoria',kwargs={"evento_id":evento.id}))
    else:
        return render(request,'evento_no_transmitir.html')