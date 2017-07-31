from django.template.loader import  render_to_string

from home.emails import send_email_hola


def email_productos(request,compra):
    bandera = False
    for detalle in compra.get_detalle():
        if not detalle.get_producto().get_tipo().es_libro_fisico():
            bandera=True
            break
    context = {'compra': compra,"digital":bandera}

    subject = "Aqui tienes tus  productos " + compra.get_nombre() + "."
    message_html = render_to_string("email/productos.html",context,request)
    message = render_to_string("email/productos.txt",context,request)
    send_email_hola(email=compra.get_email(), subject=subject,message=message, message_html=message_html)


def email_envio(request,compra):
    context = {"compra":compra}
    subject = compra.get_nombre() +" tus productos fueron enviados!"
    message = render_to_string("email/email_envio.txt",context,request)
    message_html = render_to_string("email/email_envio.html",context,request)

    send_email_hola(email=compra.get_email(), subject=subject,message=message, message_html=message_html)
