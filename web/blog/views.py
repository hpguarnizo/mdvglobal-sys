from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from accounts.models import _generate_code
from blog.emails import email_verify_suscriptor, email_welcome_blog
from blog.forms import SubscriberForm
from blog.models import CodeValidatorBlog, Subscriber


class BlogView(TemplateView):
    template_name = 'blog.html'

class AboutView(TemplateView):
    template_name = 'blog_about.html'

def PostAtraerView(request):
    template_name = 'blog_post_atraer.html'
    subscriber = False
    if request.method == 'POST':
        form = SubscriberForm(request.POST)

        if form.is_valid():
            subscriber = form.save(commit=False)
            aux_subscriber = Subscriber.objects.filter(email=subscriber.get_email())
            if len(aux_subscriber) == 0:
                subscriber.save()
            else:
                subscriber = aux_subscriber[0]
                if subscriber.confirmed and subscriber.subscribe_email:
                    form.add_error("email", "El email ya se encuentra registrado")
                    return render(request,template_name,{'form':form,'exist': True})
                else:
                    subscriber.subscribe_email = True
                    subscriber.save()
                    code = CodeValidatorBlog.objects.filter(subscriber=subscriber)
                    code.delete()

            code = CodeValidatorBlog(code=_generate_code(), subscriber=subscriber)
            code.save()

            email_verify_suscriptor(code, subscriber)
            subscriber = True
    else:
        form = SubscriberForm()

    return render(request,template_name,{'form':form,'suscripto':subscriber})

def BlogUnsubscribe(request):
    cod = request.GET.get('cod','')
    subscriptors = Subscriber.objects.get(email=cod)
    subscriptors.set_subscribe_email(False)
    subscriptors.save()
    return render(request, 'blog_unsubscribe.html', {'email': subscriptors.email})

def VerifyEmail(request):
    code = request.GET.get('code', '')
    code = code[2:len(code) - 1]
    code_validator = CodeValidatorBlog.objects.filter(code=code)

    # Handle other error responses from API
    if len(code_validator) != 1:
        return render(request,'blog_not_confirmed_email.html')

    suscriptor = code_validator.first().susciptor.activate_email()

    code = CodeValidatorBlog.objects.filter(subscriber=suscriptor)
    code.delete()

    email_welcome_blog(suscriptor)

    return render(request,'blog_confirmed_email.html')

