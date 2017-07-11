from django import forms
from django.forms import ModelForm

from accounts.models import MyUser


class MyUserForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name','last_name','photo','email']

        widgets = {
            'first_name' : forms.TextInput(attrs={'placeholder':'Nombre', 'required': True,'class': 'form-control b-r-xl'}),
            'last_name' : forms.TextInput(attrs={'placeholder': 'Apellido', 'required': True, 'class': 'form-control b-r-xl'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control b-r-xl', 'type':'email'}),

        }
