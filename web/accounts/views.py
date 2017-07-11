from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from accounts.models import MyUser, CodeValidator, _generate_code
from django.views.generic import FormView
from accounts.forms import MyUserForm
from home.emails import email_verify_password



def PerfilView(request):
    template_name = 'accounts_perfil.html'
    user = request.user
    edit = False
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():

            user.set_datos(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                           photo=form.cleaned_data['photo'])

            email = form.cleaned_data['email']
            if email != None and user.email != email:
                user = MyUser.objects.filter(email=email)
                if len(user) == 0:
                    user.set_email(email)
                    user.set_verify_email(False)
                    code = CodeValidator(code=_generate_code(), user=user)
                    code.save()
                    email_verify_password(code, user)
                else:
                    form.add_error("email", "El email ya se encuentra registrado")
            edit = True
            user.save()
    else:
        form = MyUserForm(instance=user)

    return render(request,template_name,{'form':form,'edit':edit})

def DeleteUser(request):
    user = request.user
    user.set_is_active(False)
    user.save()

    return HttpResponseRedirect(reverse('logout_page'))

