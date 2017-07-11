from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template.loader import get_template


def email_verify_suscriptor(code,suscriptor):
    url = 'http://www.codipay.co' + reverse('blog_verify_email') + '?code=' + str(code.code)
    context = {'url': url, 'cod': "%s" %suscriptor.email}

    message_html = get_template("email/blog_confirmation.html").render(context)
    subject = "Hola. Por favor confirma tu correo electrónico."
    message = get_template("email/blog_confirmation.txt").render(context)

    send_email_hola(email=suscriptor.email, subject=subject,message=message, message_html=message_html,subscriptor=suscriptor,passed=True)

def email_welcome_blog(subscriptor):
    context = {'url_panel': 'http://www.codipay.co' + reverse('signup_page_trial'),'cod': "%s" %subscriptor.email}

    message_html = get_template("email/blog_welcome.html").render(context)
    subject = "Hola. Te damos la bienvenida al Blog de Codipay."
    message = get_template("email/blog_welcome.txt").render(context)

    send_email_hola(email=subscriptor.email, subject=subject,message=message, message_html=message_html,subscriptor=subscriptor)


def send_email_hola(email, subject,message, message_html,from_email="Codipay",subscriptor=None,passed=False):
    send_email(email,subject,message,message_html,from_email,settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD,subscriptor=subscriptor,passed=passed)


def send_email(email,subject,message,message_html,from_email,auth_user,auth_password,subscriptor,passed):
    if (subscriptor.confirmed and subscriptor.subscribe_email) or passed:
        if settings.PRODUCTION:

            send_mail(subject=subject,message=message, from_email=auth_user,auth_user=auth_user,auth_password=auth_password,
                      recipient_list=[email] ,fail_silently=True,html_message=message_html)
        else:
            send_mail(subject=subject, message=message, from_email=auth_user, auth_user=settings.EMAIL_HOST_USER_DEBUG,
                      auth_password=settings.EMAIL_HOST_PASSWORD_DEBUG,
                      recipient_list=[email], fail_silently=False, html_message=message_html)
