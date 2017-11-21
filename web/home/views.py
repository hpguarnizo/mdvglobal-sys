from __future__ import absolute_import

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

from accounts.models import MyUser, CodeValidator, _generate_code
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView

from contenido.models import Contenido
from donacion.models import Donacion, Pagina
from evento.models import Evento, Entrada
from home.emails import email_verify_password, email_welcome, email_contact_technical, \
    email_contact_commercial
from tienda.models import Producto, Compra
from .forms import SignupForm, LoginForm, SupportForm

def Usuarios(request):
    return render(request,'home_clientes.html',{'usuarios':MyUser.objects.all()})

def IndexView(request):
    cant_eventos = Evento.objects.filter(estado=3).__len__
    cant_productos = Producto.objects.all().__len__
    cant_contenido = Contenido.objects.all().__len__
    return render(request,'index.html',{'cant_eventos':cant_eventos,'cant_productos':cant_productos,
                                        'cant_contenido':cant_contenido})


def JuanBallistreri(request):
    contenidos = (Contenido.objects.filter(acceso=1).order_by("-fecha") | \
                  Contenido.objects.filter(acceso=2).order_by("-fecha") |\
                  Contenido.objects.filter(acceso=3).order_by("-fecha"))[:6]
    return render(request,'juan_ballistreri.html',{"contenidos":contenidos})


def PanelUsuario(request):
    user = request.user
    request.user.finalizo_suscripcion()
    exito=request.GET.get("exito","")
    return render(request,'home_panel.html',{'entradas':Entrada.objects.filter(user=user,evento__estado__in=[1,2]),
                                             'producthttp://example.comos':Compra.objects.filter(user=user).order_by("-fecha"),"exito":exito})

def SignupView(request):
    template_name = 'home_signup.html'
    form_class = SignupForm

    if request.method=="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = MyUser.objects.filter(email=email)
            if len(user)==0:
                user = MyUser.objects.create_user(email=email,password=password,first_name=first_name,username=email,
                                                  verify_email= False)

            else:
                user=user[0]
                if user.verify_email:
                    form.add_error("email","El email ya se encuentra registrado")
                    return render(request, template_name, {'form': form})
                else:
                    code = CodeValidator.objects.filter(user=user)
                    code.delete()

            code = CodeValidator(code=_generate_code(), user=user)
            code.save()

            email_verify_password(code,user)

            return HttpResponseRedirect(reverse('signup_email_sent_page',kwargs={"email":email}))
    else:
        form = SignupForm()
    return render(request,template_name,{'form':form})


class SignupEmailSentView(TemplateView):
    template_name = 'home_signup_email_sent.html'

    def get(self, request,email, *args, **kwargs):
        return render(request,self.template_name,{"email":email})


class PremiumOkView(TemplateView):
    template_name = 'pay_premium_ok.html'

    def get_context_data(self, **kwargs):
        context = super(PremiumOkView, self).get_context_data(**kwargs)
        user = self.request.user
        #Code custom here
        context['isactive'] = user.get_is_active()
        return context


class SignupVerifyView(View):
    def get(self, request, format=None):
        code = request.GET.get('code', '')
        code = code[2:len(code)-1]
        code_validator = CodeValidator.objects.filter(code=code)

        # Handle other error responses from API
        if len(code_validator)!=1:
            return HttpResponseRedirect(reverse('signup_not_verified_page'))

        user = code_validator.first().user.activate_email()

        code = CodeValidator.objects.filter(user=user)
        code.delete()

        email_welcome(user)

        return HttpResponseRedirect(reverse('signup_verified_page'))


class LoginView(FormView):
    template_name = 'home_login.html'
    form_class = LoginForm

    def get(self, request,**kwargs):
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseRedirect(reverse('home_panel'))
        return render(request,self.template_name,{'form':LoginForm()})

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(username=email, password=password)
        if user is not None and user.verify_email:
            if not user.is_active:
                user.set_is_active(True)
                user.save()
            login(self.request, user)

        else:
            # Return an 'invalid login' error message.
            form.add_error("email","El email o password son invalidos")
            return self.form_invalid(form)

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('home')
        else:
            return reverse('home_panel')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('inicio'))


class TermsAndPrivacityView(TemplateView):
    template_name = 'home_terms_and_privacity.html'


def Support(request):
    consult_send = False
    context = {}
    if request.method == 'POST':
        form = SupportForm(request.POST,request.FILES)

        if form.is_valid():
            contact = form.save()
            if contact.get_motive().is_commercial():
                email_contact_commercial(contact)
            else:
                email_contact_technical(contact)
            consult_send=True
    else:
        form = SupportForm()

    context['consult_send'] = consult_send
    context['form'] = form
    return render(request, 'home_support.html',context)


class SignupNotVerified(TemplateView):
    template_name = 'home_signup_not_verified.html'


class SignupVerified(TemplateView):
    template_name = 'home_signup_verified.html'


def Unsubscribe(request):
    user = request.user
    user.set_subscribe_email(False)
    user.save()

    return render(request,'home_unsubscribe.html',{})

class Home(TemplateView):
    template_name = 'home_home.html'