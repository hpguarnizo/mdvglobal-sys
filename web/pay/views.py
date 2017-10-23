from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import mercadopago
import json
from donacion.models import Donacion, Pagina
from evento.emails import email_entrada_nueva
from evento.models import Entrada
from pay.forms import PlanesConfigForm
from pay.models import Customer, Premium, Gratis, Ministerial
import os
from tienda.models import Compra


class HomePayView(TemplateView):
    template_name = 'pay_plans.html'


def PlanesForm(request):
    if request.method=="POST":
        form = PlanesConfigForm(request.POST)
        if form.is_valid():
            pass
    else:
        form=PlanesConfigForm(initial={"gratis":Gratis.objects.all().first().get_cost(),
                                       "premium":Premium.objects.all().first().get_cost(),
                                       "ministerial":Ministerial.objects.all().first().get_cost()})
    return render(request,'pay_configuracion.html',{'form':form})


def buy_my_item(request):
    code = None
    description = None
    user = request.user
    if request.POST.get('token',''):
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))

        dic = {
            "transaction_amount": 97,
            "token": "%s" %request.POST.get('token',''),
            "installments": 1,
            "description": "Crece",
            "payment_method_id": request.POST.get('paymentMethodId',''),
            "payer": {
                "email": "codicero@gmail.com"
            },
            "external_reference": user.username,
            "statement_descriptor": "CODIPAY - Año Premium",
        }
        payment = mp.post("/v1/payments", dic )
        json.dumps(payment, indent=4)

        if payment['status'] == 201:
            if payment['response']['status'] == 'approved':
                customer = Customer(user=user,plan=Premium.objects.all().first())
                customer.save()
                user.set_customer(customer)
                user.save()
                return HttpResponseRedirect(reverse('pay_return_url_premium'))
            else:
                description = payment['response']['status']
                code = 201
        else:
            code = payment['response']['cause'][0]['code']
            description = payment['response']['cause'][0]['description']

    return render(request,'pay_payment.html',{'code':code,'description':description,'PUBLIC_KEY_MP': os.environ.get('PUBLIC_KEY_MP')})


def buy_my_entrada(request,entrada_id):
    entrada = get_object_or_404(Entrada,id=entrada_id)
    code = None
    description = None

    if request.POST.get('token',''):
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))
        dic = {
            "transaction_amount": entrada.get_evento().get_precio(),
            "token": "%s" %request.POST.get('token',''),
            "installments": 1,
            "description": entrada.get_evento().get_nombre(),
            "payment_method_id": request.POST.get('paymentMethodId',''),
            "payer": {
                "email": os.environ.get("EMAIL_MP")
            },
            "external_reference": entrada.id,
            "statement_descriptor": entrada.get_evento().get_nombre(),
        }
        payment = mp.post("/v1/payments", dic )
        json.dumps(payment, indent=4)

        if payment['status'] == 201:
            if payment['response']['status'] == 'approved':
                entrada.pagar(entrada)
                email_entrada_nueva(request, entrada)
                return HttpResponseRedirect(reverse('evento_comprado',kwargs={"entrada_id":entrada.id}))
            else:
                description = payment['response']['status']
                code = 201
        else:
            code = payment['response']['cause'][0]['code']
            description = payment['response']['cause'][0]['description']

    return render(request,'pay_entrada.html',{'code':code,'description':description,'PUBLIC_KEY_MP': os.environ.get('PUBLIC_KEY_MP'),
                                              "entrada":entrada})

def buy_my_premium(request):
    code = None
    description = None
    user = request.user

    if request.POST.get('token',''):
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))
        dic = {
            "transaction_amount": 150,
            "token": "%s" %request.POST.get('token',''),
            "installments": 1,
            "description": "Suscripcion Premium",
            "payment_method_id": request.POST.get('paymentMethodId',''),
            "payer": {
                "email": os.environ.get("EMAIL_MP")
            },
            "external_reference": user.id,
            "statement_descriptor": user.get_full_name(),
        }
        payment = mp.post("/v1/payments", dic )
        json.dumps(payment, indent=4)

        if payment['status'] == 201:
            if payment['response']['status'] == 'approved':

                return HttpResponseRedirect(reverse('home_panel'))
            else:
                description = payment['response']['status']
                code = 201
        else:
            code = payment['response']['cause'][0]['code']
            description = payment['response']['cause'][0]['description']

    return render(request,'pay_premium.html',{'code':code,'description':description,'PUBLIC_KEY_MP': os.environ.get('PUBLIC_KEY_MP')})

def buy_my_ministerial(request):
    code = None
    description = None
    user = request.user

    if request.POST.get('token',''):
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))
        dic = {
            "transaction_amount": 999,
            "token": "%s" %request.POST.get('token',''),
            "installments": 1,
            "description": "Suscripcion Miniterial",
            "payment_method_id": request.POST.get('paymentMethodId',''),
            "payer": {
                "email": os.environ.get("EMAIL_MP")
            },
            "external_reference": user.id,
            "statement_descriptor": user.get_full_name(),
        }
        payment = mp.post("/v1/payments", dic )
        json.dumps(payment, indent=4)

        if payment['status'] == 201:
            if payment['response']['status'] == 'approved':

                return HttpResponseRedirect(reverse('home_panel'))
            else:
                description = payment['response']['status']
                code = 201
        else:
            code = payment['response']['cause'][0]['code']
            description = payment['response']['cause'][0]['description']

    return render(request,'pay_ministerial.html',{'code':code,'description':description,'PUBLIC_KEY_MP': os.environ.get('PUBLIC_KEY_MP')})

def buy_my_productos(request,compra_id):
    compra = get_object_or_404(Compra,id=compra_id)

    code = None
    description = None
    if request.POST.get('token',''):
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))
        dic = {
            "transaction_amount": compra.total(),
            "token": "%s" %request.POST.get('token',''),
            "installments": 1,
            "description": "Compra en "+os.environ.get("COMPANY"),
            "payment_method_id": request.POST.get('paymentMethodId',''),
            "payer": {
                "email": os.environ.get("EMAIL_MP")
            },
            "external_reference": compra.id,
            "statement_descriptor": "Compra en "+os.environ.get("COMPANY"),
        }
        payment = mp.post("/v1/payments", dic )
        json.dumps(payment, indent=4)

        if payment['status'] == 201:
            if payment['response']['status'] == 'approved':
                compra.pagar()
                return HttpResponseRedirect(reverse('tienda_envio',kwargs={"compra_id":compra.id}))
            else:
                description = payment['response']['status']
                code = 201
        else:
            code = payment['response']['cause'][0]['code']
            description = payment['response']['cause'][0]['description']

    return render(request,'pay_tienda.html',{'code':code,'description':description,'PUBLIC_KEY_MP': os.environ.get('PUBLIC_KEY_MP'),
                                              "compra":compra})

def buy_my_donacion(request):
    cantidad = request.GET.get("donacion","100")
    config = Pagina.objects.all().first()
    code = None
    description = None
    if request.POST.get('token',''):
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))
        dic = {
            "transaction_amount": cantidad,
            "token": "%s" %request.POST.get('token',''),
            "installments": 1,
            "description": config.get_titulo(),
            "payment_method_id": request.POST.get('paymentMethodId',''),
            "payer": {
                "email": os.environ.get("EMAIL_MP")
            },
            "statement_descriptor": "Donacion",
        }
        payment = mp.post("/v1/payments", dic )
        json.dumps(payment, indent=4)

        if payment['status'] == 201:
            if payment['response']['status'] == 'approved':
                donacion = Donacion(monto=cantidad,nombre=request.POST.get('cardholderName','Sin Nombre'))
                donacion.save()
                return HttpResponseRedirect(reverse('donacion_gracias',kwargs={'donacion_id':donacion.id}))
            else:
                description = payment['response']['status']
                code = 201
        else:
            code = payment['response']['cause'][0]['code']
            description = payment['response']['cause'][0]['description']

    return render(request,'pay_donacion.html',{'code':code,'description':description,'PUBLIC_KEY_MP': os.environ.get('PUBLIC_KEY_MP'),
                                              "cantidad":cantidad,"donacion":config})


@csrf_exempt
def return_url_premium(request):
    return render(request,'pay_premium_ok.html',{})


@csrf_exempt
def cancel_return_premium(request):
    return render(request,'pay_plans.html',{})

