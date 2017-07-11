from django.core.urlresolvers import reverse
from django.template.loader import get_template

from home.emails import send_email_hola


def email_suscription_premium(user):
    context = {'name': user.get_first_name(), 'url': 'http://www.codipay.co' + reverse('codeqr_promotion_new')}

    message_html = get_template("email/pay_premium.html").render(context)
    subject = "Hola " + user.get_first_name() + ". ¡Felicidades! Ahora tu cuenta es Premium."
    message = get_template("email/pay_premium.txt").render(context)

    send_email_hola(email=user.email, subject=subject, message=message,message_html=message_html,user=user)


def email_sucription_cancel(user):
    context = {'name': user.get_first_name()}

    message_html = get_template("email/pay_cancel.html").render(context)
    subject = "Hola " + user.get_first_name() + ". Estamos realmente tristes por tu partida ."
    message = get_template("email/pay_cancel.txt").render(context)

    send_email_hola(email=user.email, subject=subject, message=message,message_html=message_html,user=user)


def email_content_free_plan(user):
    context = {'name': user.get_first_name()}

    message_html = get_template("email/pay_content_free_plan.html").render(context)
    subject = "La Fórmula Del Éxito Para Tu Negocio."
    message = get_template("email/pay_content_free_plan.txt").render(context)

    send_email_hola(email=user.email, subject=subject, message=message, message_html=message_html,user=user)

def email_support_free_user(user):
    context = {'name': user.get_first_name()}

    message_html = get_template("email/pay_support_free_user.html").render(context)
    subject = "Hola "+ user.get_first_name() +". ¿Estás midiendo el crecimiento de tu negocio? "
    message = get_template("email/pay_support_free_user.txt").render(context)

    send_email_hola(email=user.email, subject=subject, message=message, message_html=message_html,user=user)
