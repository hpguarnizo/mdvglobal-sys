import os
from django.template.loader import  render_to_string

from home.emails import send_email_hola


def email_verify_suscriptor(request,code,suscriptor):
    context = {'code': str(code.code)}

    message_html = render_to_string("email/blog_confirmation.html",context,request)
    subject = "Hola. Por favor confirma tu correo electrónico."
    message = render_to_string("email/blog_confirmation.txt",context,request)
    send_email_hola(email=suscriptor.email, subject=subject,message=message, message_html=message_html)

def email_welcome_blog(request,subscriptor):
    context = {"subscriptor":subscriptor}

    message_html = render_to_string("email/blog_welcome.html",context,request)
    subject = "Hola. Te damos la bienvenida al Newsletter de %s." %(os.environ.get("COMPANY"))
    message = render_to_string("email/blog_welcome.txt",context,request)
    if (subscriptor.confirmed and subscriptor.subscribe_email):
        send_email_hola(email=subscriptor.email, subject=subject,message=message, message_html=message_html)

