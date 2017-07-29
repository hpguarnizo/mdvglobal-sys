import os

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.core.mail import send_mail
from django.conf import settings

def email_notify_change_password(user):
    context = {'name': user.get_first_name(),
                 'url':  Site.objects.get_current().domain + reverse('signup_page'), 'company':os.environ.get("COMPANY","")}
    mensaje = get_template("email/home_confirm_password.html").render(context)
    asunto = "Confirmación Cambio de Contraseña"

    send_email_hola(email=user.email, asunto=asunto, mensaje=mensaje)


def email_verify_password(code,user):
    url =  Site.objects.get_current().domain + reverse('signup_verify') + '?code=' + str(code.code)
    context = {'name': user.get_first_name(),'url': url, 'company':os.environ.get("COMPANY","")}

    message_html = get_template("email/home_signup.html").render(context)
    subject = "Hola " + user.get_first_name() + ". Por favor confirma tu correo electrónico."
    message = get_template("email/home_signup.txt").render(context)

    send_email_hola(email=user.email, subject=subject,message=message, message_html=message_html)


def email_welcome(user):
    context = {'name': user.get_first_name(),'url_panel':  Site.objects.get_current().domain + reverse('turn_all'),
               'company':os.environ.get("COMPANY","")}

    message_html = get_template("email/home_welcome.html").render(context)
    subject = "Hola " + user.get_first_name() + ". Te damos la bienvenida a Codipay."
    message = get_template("email/home_welcome.txt").render(context)

    send_email_hola(email=user.email, subject=subject,message=message, message_html=message_html)


def email_contact_technical(contact):
    context = {'contact': contact}

    message_html = ""
    subject = "Soporte Tecnico"
    message = get_template("email/home_contact.txt").render(context)
    if not settings.DEBUG:
        send_email_soporte(email=settings.EMAIL_HOST_USER, subject=subject, message=message, message_html=message_html)
    else:
        send_email_hola(email=settings.EMAIL_HOST_USER, subject=subject, message=message, message_html=message_html)


def email_contact_commercial(contact):
    context = {'contact': contact}

    message_html = ""
    subject = "Soporte Comercial"
    message = get_template("email/home_contact.txt").render(context)
    if not settings.DEBUG:
        send_email_felicidad(email=settings.EMAIL_HOST_USER, subject=subject, message=message, message_html=message_html)
    else:
        send_email_hola(email=settings.EMAIL_HOST_USER, subject=subject, message=message, message_html=message_html)


def send_email_hola(email, subject,message, message_html,from_email="Company",user=None):
    send_email(email,subject,message,message_html,from_email,settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)


def send_email_soporte(email, subject,message, message_html,user=None):
    send_email(email,subject,message,message_html,"Soporte",settings.EMAIL_HOST_USER_SOPORTE,settings.EMAIL_HOST_PASSWORD_SOPORTE)


def send_email_felicidad(email, subject,message, message_html,user=None):
    send_email(email,subject,message,message_html,"Felicidad",settings.EMAIL_HOST_USER_FELICIDAD,settings.EMAIL_HOST_PASSWORD_FELICIDAD)


def send_email(email,subject,message,message_html,from_email,auth_user,auth_password,user=None):
    if user == None or (user != None and user.subscribe_email):
        if not settings.DEBUG:
            send_mail(subject=subject,message=message, from_email=auth_user,auth_user=auth_user,auth_password=auth_password,
                      recipient_list=[email] ,fail_silently=False,html_message=message_html)
        else:
            send_mail(subject=subject, message=message,from_email="", auth_user=settings.EMAIL_HOST_USER,
                      auth_password=settings.EMAIL_HOST_PASSWORD,
                      recipient_list=[email], fail_silently=False, html_message=message_html)