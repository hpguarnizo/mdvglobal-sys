from django import forms
from django.forms.forms import NON_FIELD_ERRORS

from home.models import Contact


class FormularioConsulta(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"type":"email","class":"form-control campo-form-contacto ",
                                                           "placeholder":"E-mail de contacto","required":True}))
    consulta = forms.CharField(max_length=5000,min_length=5,widget=forms.TextInput(attrs={"class":"form-control campoconsulta "
                                                                                                   "campo-form-contacto", "placeholder":
                                                                                           "Ingrese su consulta", 'required':True}))
    nombre = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class':'form-control','required':True, 'type':'text'}))


class AddErrorMixin(object):
    def add_error(self, field, msg):
        field = field or NON_FIELD_ERRORS
        if field in self._errors:
            self._errors[field].append(msg)
        else:
            self._errors[field] = self.error_class([msg])


class PasswordForm(AddErrorMixin, forms.Form):

    password = forms.CharField(max_length=128, widget=forms.TextInput(attrs={"type":"password","class":"center-block campo-form ",
                                                           "placeholder":"Password","required":True}))


class SignupForm(PasswordForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"type":"text",
                                                                                             "class":"center-block campo-form",
                                                                                             "placeholder":"Nombre",
                                                                                             "required":True}))
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={"type":"email",
                                                                           "class":"center-block campo-form",
                                                                            "placeholder":"E-mail",
                                                                           "required":True}))


class LoginForm(AddErrorMixin, forms.Form):
    email = forms.EmailField(max_length=255,widget=forms.TextInput(attrs={"type":"email","class":"center-block campo-form",
                                                           "placeholder":"E-mail","required":True}))
    password = forms.CharField(max_length=128,widget=forms.TextInput(attrs={"type":"password","class":"center-block campo-form ",
                                                           "placeholder":"Password","required":True}))


class PasswordResetForm(AddErrorMixin, forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={"type":"email",
                                                                           "class":"center-block campo-form form-control",
                                                                           "placeholder":"E-mail",
                                                                           "required":True}))


class PasswordResetVerifiedForm(PasswordForm):
    pass


class PasswordChangeForm(PasswordForm):
    password = forms.CharField(max_length=128,
                               widget=forms.TextInput(attrs={"type": "password", "class": "form-control",
                                                             "placeholder": "Nueva contraseña", "required": True}))
    password2 = forms.CharField(max_length=128,
                                widget=forms.TextInput(attrs={"type": "password", "class": "form-control",
                                                              "placeholder": "Confirma tu nueva contraseña", "required": True}))



class SupportForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['title','description','image','motive']
        widgets = {
            'title': forms.TextInput(attrs={'required': True, 'class': 'form-control b-r-xl'}),
            'description': forms.TextInput(attrs={'required': True, 'class': 'form-control b-r-xl'}),
            'motive': forms.Select(attrs={'class':'form-control m-b b-r-xl'})
        }


