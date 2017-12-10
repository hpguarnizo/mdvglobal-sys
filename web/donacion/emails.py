from django.template.loader import render_to_string
from donacion.models import Pagina
from home.emails import send_email_hola



def email_donacion(request,donacion):
    context = {'pagina':Pagina.objects.all().first()}
    message_html = render_to_string("email/email_donacion.html",context,request)
    message = render_to_string("email/email_donacion.txt",context,request)
    subject = "¡Gracias por tu donacion!"

    send_email_hola(email=donacion.get_nombre(), subject=subject, message=message, message_html=message_html)
