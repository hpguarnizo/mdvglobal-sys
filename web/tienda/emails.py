from django.template.loader import get_template

from home.emails import send_email_hola


def email_productos(email,nombre,compra):
    context = {'nombre': nombre,}

    message_html = get_template("email/productos.html").render(context)
    subject = "Aqui tienes tus  productos " + nombre + "."
    message = get_template("email/productos.txt").render(context)

    send_email_hola(email=email, subject=subject,message=message, message_html=message_html)
