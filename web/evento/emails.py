import os

from django.template.loader import get_template

from accounts.models import MyUser
from home.emails import send_email_hola


def email_evento_nuevo(evento):
    for user in MyUser.objects.filter(is_staff=False):
        context = {'nombre': evento.get_nombre(),
                   'url': evento.get_url(),
                   'company': os.environ.get("COMPANY", "")}
        message_html = get_template("email/evento_nuevo.html").render(context)
        message = get_template("email/evento_nuevo.txt").render(context)
        subject = "Nuevo Evento"

        send_email_hola(email=user.email, subject=subject, message=message, message_html=message_html)

def email_entrada_nueva(entrada):
    context = {'entrada':entrada,
                   'company': os.environ.get("COMPANY", "")}
    message_html = get_template("email/entrada_nueva.html").render(context)
    message = get_template("email/entrada_nueva.txt").render(context)
    subject = "Nueva Entrada"

    send_email_hola(email=entrada.get_email(), subject=subject, message=message, message_html=message_html)
