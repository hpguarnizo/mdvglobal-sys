from django.template.loader import render_to_string
from accounts.models import MyUser
from blog.models import Subscriber
from home.emails import send_email_hola


def email_evento_nuevo(request,evento):
    for user in MyUser.objects.filter():
        context = {'evento': evento,"nombre":user.get_full_name()}
        message_html = render_to_string("email/evento_nuevo.html",context,request)
        message = render_to_string("email/evento_nuevo.txt",context,request)
        subject = "Hola %s, nos complace anunciarte que tenemos una nueva convocatoria." %user.get_full_name()

        send_email_hola(email=user.email, subject=subject, message=message, message_html=message_html)
    for sus in Subscriber.objects.all():
        if sus.get_subscribe_email():
            context = {'evento': evento, "nombre": sus.get_email()}
            message_html = render_to_string("email/evento_nuevo.html", context, request)
            message = render_to_string("email/evento_nuevo.txt", context, request)
            subject = "Hola , nos complace anunciarte que tenemos una nueva convocatoria."
            send_email_hola(email=user.email, subject=subject, message=message, message_html=message_html)


def email_entrada_nueva(request,entrada):
    context = {'entrada':entrada,}
    message_html = render_to_string("email/entrada_nueva.html",context,request)
    message = render_to_string("email/entrada_nueva.txt",context,request)
    subject = "Felicitaciones %s, aqui tienes tu entrada." %(entrada.get_nombre())

    send_email_hola(email=entrada.get_email(), subject=subject, message=message, message_html=message_html)


def email_entrada_pago(request,entrada):
    context = {'entrada':entrada,}
    message_html = render_to_string("email/entrada_pago.html",context,request)
    message = render_to_string("email/entrada_pago.txt",context,request)
    subject = "Solo un paso mas %s." %(entrada.get_nombre())

    send_email_hola(email=entrada.get_email(), subject=subject, message=message, message_html=message_html)


def email_evento_inicia(request,evento):
    for entrada in evento.get_entradas():
        context = {'entrada':entrada,}
        message_html = render_to_string("email/evento_inicia.html",context,request)
        message = render_to_string("email/evento_inicia.txt",context,request)
        subject = "Apresurate %s que ya comenzo la convocatoria." %(entrada.get_nombre())

        send_email_hola(email=entrada.get_email(), subject=subject, message=message, message_html=message_html)


