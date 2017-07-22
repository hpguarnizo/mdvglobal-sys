from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from donacion.forms import CantidadForm, PaginaForm
from donacion.models import Pagina, Donacion as D, Donacion
from tienda.views import get_compra


def VerDonaciones(request):
    return render(request,'donacion_lista.html',{'donaciones':D.objects.all().order_by('fecha')})

def Configurar(request):
    guardado = False
    pagina = Pagina.objects.all()
    if request.method=="POST":
        form = PaginaForm(request.POST)
        if form.is_valid():
            if len(pagina)>0:
                pagina = pagina.first()
                pagina.set_data(form.save(commit=False))
            else:
                form.save()
            guardado=True
    else:
        if len(pagina)>0:
            form = PaginaForm(instance=pagina.first())
        else:
            form = PaginaForm()
    return render(request,'donacion_configuracion.html',{'form':form,'guardado':guardado})


def DonacionVista(request):
    if request.method=="POST":
        form = CantidadForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            return HttpResponseRedirect(reverse('pay_donacion')+"?cantidad=%f" %cantidad)
    else:
        form = CantidadForm()
    return render(request,'donacion.html',{'form':form,'donacion':Pagina.objects.all().first(),"compra":get_compra(request)})

def DonacionGracias(request,donacion_id):
    donacion = get_object_or_404(Donacion,id=donacion_id)
    return render(request,'donacion_gracias.html',{"donacion":donacion,"compra":get_compra(request)})