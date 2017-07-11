from django.forms import ModelForm
from django import forms
from blog.models import Subscriber


class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Tu Email', 'required': True,
                       'class': 'form-control email', 'type': 'email', }),
        }
