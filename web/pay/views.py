from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import mercadopago
import json

from accounts.models import MyUser
from donacion.models import Donacion, Pagina
from evento.emails import email_entrada_nueva
from evento.models import Entrada
from pay.forms import PlanesConfigForm
from pay.models import Customer, Premium, Gratis, Ministerial
import os
from tienda.models import Compra
from django.http import HttpResponse


def HomePayView(request):
    template_name = 'pay_plans.html'
    return render(request,template_name,{"premium":Premium.objects.all().first(),"ministerial":Ministerial.objects.all().first()})


def PlanesForm(request):
    edit=False
    error=""
    if request.method=="POST":
        form = PlanesConfigForm(request.POST)
        if form.is_valid():
            premium = Premium.objects.all().first()
            ministerial = Ministerial.objects.all().first()

            premium.set_cost(form.cleaned_data["premium"])
            ministerial.set_cost(form.cleaned_data["ministerial"])

            mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))

            if premium.esta_creado():
                plan = mp.put("/v1/plans/"+premium.get_id_mp(), {"auto_recurring": {"transaction_amount": premium.get_cost()}})
                if plan['status'] == 200:
                    premium.save()
                else:
                    error = plan['response']['cause'][0]['code'] + ":" + plan['response']['cause'][0][
                        'description'] + "/n"
            else:
                dic = {
                    "status": "active",
                    "description": "Suscripcion Premium a Manantial de Vida",
                    "external_reference":premium.id,
                    "auto_recurring": {
                        "frequency": 1,
                        "frequency_type": "months",
                        "transaction_amount": premium.get_cost(),
                    },
                }
                plan= mp.post("/v1/plans", dic)
                json.dumps(plan, indent=4)
                if plan['status']==201:
                    premium.set_id_mp(plan["response"]["id"])
                    premium.save()
                else:
                    error = plan['response']['cause'][0]['code'] + ":"+ plan['response']['cause'][0]['description']+ "/n"

            if ministerial.esta_creado():
                plan = mp.put("/v1/plans/"+ministerial.get_id_mp(),
                                                     {"auto_recurring": {"transaction_amount": ministerial.get_cost()}})
                if plan['status'] == 200:
                    ministerial.save()
                else:
                    error+= plan['response']['cause'][0]['code'] + ":" + plan['response']['cause'][0][
                        'description'] + "/n"

            else:
                dic = {
                    "status": "active",
                    "description": "Suscripcion Ministerial a Manantial de Vida",
                    "external_reference":ministerial.id,
                    "auto_recurring": {
                        "frequency": 1,
                        "frequency_type": "months",
                        "transaction_amount": ministerial.get_cost(),
                    },
                }
                plan= mp.post("/v1/plans", dic)
                json.dumps(plan, indent=4)
                if plan['status']==201:
                    ministerial.set_id_mp(plan["response"]["id"])
                    ministerial.save()
                else:
                    error+= plan['response']['cause'][0]['code'] + ":"+ plan['response']['cause'][0]['description']+ "/n"

            edit = True
    else:
        form=PlanesConfigForm(initial={"premium":Premium.objects.all().first().get_cost(),
                                       "ministerial":Ministerial.objects.all().first().get_cost()})
    return render(request,'pay_configuracion.html',{'form':form,"edit":edit,"error":error})


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
                "email": request.POST.get("email")
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
    premium=Premium.objects.all().first()
    if request.POST.get('token',''):
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))
        dic = {
            "transaction_amount": 1,
            "token": "%s" % request.POST.get('token', ''),
            "installments": 1,
            "description": "Prueba de tarjeta",
            "payment_method_id": request.POST.get('paymentMethodId', ''),
            "payer": {
                "email": request.POST.get("email")
            },
            "capture": False
        }
        payment = mp.post("/v1/payments", dic)
        json.dumps(payment, indent=4)

        if payment['status'] == 201:
            if payment['response']['status'] == 'authorized':

                if user.get_customer_id():
                    customer_id= user.get_customer_id()
                else:
                    customer = mp.get("/v1/customers/search", {"email": user.get_email()})
                    json.dumps(customer, indent=4)
                    if customer["response"]["results"][0]["id"]:
                        customer_id = customer["response"]["results"][0]["id"]
                        user.set_customer_id(customer_id)
                        user.save()
                    else:
                        customer = mp.post("/v1/customers", {"email": request.POST.get('email','')})
                        json.dumps(customer, indent=4)
                        customer_id = customer["response"]["results"][0]["id"]
                        user.set_customer_id(customer_id)
                        user.save()

                mp.post("/v1/customers/" + customer_id + "/cards", {"token": request.POST.get('token','')})
                suscription= mp.post("/v1/subscriptions/",{"plan_id":premium.get_id_mp(),
                                                           "payer":{
                                                               "id":customer_id
                                                           }})
                if suscription['status'] == 201:
                    if suscription['response']['status'] == 'authorized':
                        user.premium()
                        return HttpResponseRedirect(reverse('home_panel'))
                    else:
                        description = suscription['response']['status']
                        code = 201
                else:
                    code = suscription['response']['cause'][0]['code']
                    description = suscription['response']['cause'][0]['description']
            else:
                code = payment['response']['status']
                description = "Tarjeta no autorizada"
        else:
            code = payment['response']['status']
            description = "Tarjeta no autorizada"

    return render(request,'pay_premium.html',{'code':code,'description':description,
                                              'PUBLIC_KEY_MP': os.environ.get('PUBLIC_KEY_MP'),"premium":premium})

def buy_my_ministerial(request):
    code = None
    description = None
    user = request.user
    ministerial=Ministerial.objects.all().first()
    if request.POST.get('token',''):
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))
        mp.sandbox_mode(True)
        dic = {
            "transaction_amount": 1,
            "token": "%s" % request.POST.get('token', ''),
            "installments": 1,
            "description": "Prueba de tarjeta",
            "payment_method_id": request.POST.get('paymentMethodId', ''),
            "payer": {
                "email": request.POST.get("email")
            },
             "capture": False
        }
        payment = mp.post("/v1/payments", dic)
        json.dumps(payment, indent=4)

        if payment['status'] == 201:
            if payment['response']['status'] == 'authorized':
                if user.get_customer_id():
                    customer_id= user.get_customer_id()
                    customer = mp.get("/v1/customers/search", {"email": user.get_email()})
                    json.dumps(customer, indent=4)
                else:
                    customer = mp.get("/v1/customers/search", {"email": user.get_email()})
                    json.dumps(customer, indent=4)
                    if customer["response"]["results"][0]["id"]:
                        customer_id = customer["response"]["results"][0]["id"]
                        user.set_customer_id(customer_id)
                        user.save()
                    else:
                        customer = mp.post("/v1/customers", {"email": request.POST.get('email','')})
                        json.dumps(customer, indent=4)
                        customer_id = customer["response"]["results"][0]["id"]
                        user.set_customer_id(customer_id)
                        user.save()

                mp.post("/v1/customers/" + customer_id + "/cards", {"token": request.POST.get('token','')})
                suscription= mp.post("/v1/subscriptions/",{"plan_id":ministerial.get_id_mp(),
                                                   "payer":{
                                                       "id":customer_id
                                                   }})
                if suscription['status'] == 201:
                    if suscription['response']['status'] == 'authorized':
                        user.ministerial()
                        return HttpResponseRedirect(reverse('home_panel'))
                    else:
                        description = suscription['response']['status']
                        code = 201
                else:
                    code = suscription['response']['cause'][0]['code']
                    description = suscription['response']['cause'][0]['description']
            else:
                code = payment['response']['status']
                description = "Tarjeta no autorizada"
        else:
            code = payment['response']['status']
            description = "Tarjeta no autorizada"
    return render(request,'pay_ministerial.html',{'code':code,'description':description,
                                                  'PUBLIC_KEY_MP': os.environ.get('PUBLIC_KEY_MP'),
                                                  "ministerial":ministerial})


def notifications(request,**kwargs):
    if request.method=="POST":
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))
        paymentInfo = mp.get_payment_info(kwargs["id"])
        if paymentInfo["response"]["status"] == "unpaid" or paymentInfo["response"]["status"] == "cancelled":
            user = MyUser.objects.get(customer_id_mp=paymentInfo["response"]["payer"]["id"])
            user.finalizo_suscripcion()
        elif paymentInfo["response"]["status"] == "paid":
            user = MyUser.objects.get(customer_id_mp=paymentInfo["response"]["payer"]["id"])
            user.renovar_suscripcion()
    return HttpResponse(status=200)

def buy_my_productos(request,compra_id):
    compra = get_object_or_404(Compra,id=compra_id)
    if not compra.verificar_libros():
        return HttpResponseRedirect(reverse('tienda_carrito'))
    
    code = None
    description = None
    if request.POST.get('token',''):
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))
        dic = {
            "transaction_amount": compra.get_total(),
            "token": "%s" %request.POST.get('token',''),
            "installments": 1,
            "description": "Compra en "+os.environ.get("COMPANY"),
            "payment_method_id": request.POST.get('paymentMethodId',''),
            "payer": {
                "email": compra.get_email()
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
    return render(request,'pay_tienda_2.html',{'code':code,'description':description,'PUBLIC_KEY_MP': os.environ.get('PUBLIC_KEY_MP'),
                                              "compra":compra})

def buy_my_donacion(request):
    cantidad = float(request.GET.get("cantidad","100"))
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
                "email": request.POST.get("email")
            },
            "statement_descriptor": config.get_titulo() +" - Donacion",
        }
        payment = mp.post("/v1/payments", dic )
        json.dumps(payment, indent=4)

        if payment['status'] == 201:
            if payment['response']['status'] == 'approved':
                donacion = Donacion(monto=cantidad,nombre=request.POST.get('email'))
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



def cancel_suscription(request):
    user = request.user
    mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))
    cancel = mp.cancel_preapproval_payment(user.get_customer_id())
    json.dumps(cancel, indent=4)
    if cancel['status']==201:
        user.desuscribir()
        return HttpResponseRedirect(reverse('home_panel')+"?exito=true")
    else:
        return HttpResponseRedirect(reverse('home_panel')+"?exito=true")

@csrf_exempt
def return_url_premium(request):
    return render(request,'pay_premium_ok.html',{})


@csrf_exempt
def cancel_return_premium(request):
    return render(request,'pay_plans.html',{})

