from cities_light.models import City, Region, Country
from django import forms
from evento.models import Evento, Entrada


class FormEvento(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'imagen', 'fecha', 'cupo', 'precio', 'categoria', 'direccion', 'ciudad',
                  'tipo_evento', 'provincia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control b-r-xl', 'required': True, "maxlength": "256"}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control b-r-xl', 'required': True}),
            'fecha': forms.DateInput(attrs={'class': 'form-control b-r-xl', 'required': True}),
            'cupo': forms.NumberInput(
                attrs={'class': 'form-control b-r-xl presencial', "min": "1", "placeholder": "50"}),
            'precio': forms.NumberInput(attrs={'class': 'form-control b-r-xl', "min": "0", "placeholder": "47.99"}),
            'categoria': forms.Select(attrs={'class': 'form-control b-r-xl', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control b-r-xl presencial', "maxlength": "256"}),
            'ciudad': forms.Select(attrs={'class': 'form-control b-r-xl'}),
            'provincia': forms.Select(attrs={'class': 'form-control b-r-xl presencial'}),
            'tipo_evento': forms.Select(attrs={'class': 'form-control b-r-xl', 'required': True}),
        }

    def __init__(self,*args, **kwargs):
        super(FormEvento, self).__init__(*args,**kwargs)
        self.fields["ciudad"].choices = City.objects.none()
        self.fields["provincia"].choices = Region.objects.none()

class FormEventoEdit(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'imagen', 'cupo', 'precio', 'direccion',"fecha"]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control b-r-xl', 'required': True, "maxlength": "256"}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control b-r-xl', 'required': True}),
            'cupo': forms.NumberInput(
                attrs={'class': 'form-control b-r-xl presencial', "min": "1", "placeholder": "50"}),
            'precio': forms.NumberInput(attrs={'class': 'form-control b-r-xl', "min": "0", "placeholder": "47.99"}),
            'direccion': forms.TextInput(attrs={'class': 'form-control b-r-xl presencial', "maxlength": "256"}),
            'fecha': forms.DateInput(attrs={'class': 'form-control b-r-xl', 'required': True}),
        }


class PerfilCompletar(forms.Form):
    pais = forms.ModelChoiceField(queryset=Country.objects.all(),widget=forms.Select(attrs={'class':'form-control b-r-xl',
                                                                                            'required':True}))
    provincia = forms.ModelChoiceField(queryset=Region.objects.none(),widget=forms.Select(attrs={'class':'form-control b-r-xl',
                                                                                              'required':True}))
    email = forms.EmailField(required=False)


class EntradaForm(forms.ModelForm):
    class Meta:
        model=Entrada
        fields=["nombre","email","provincia"]
        widgets={
            "nombre":forms.TextInput(attrs={"class":"form-control b-r-xl","required":True,"placeholder":"Nombre"}),
            "email":forms.EmailInput(attrs={"class":"form-control b-r-xl","required":True,"placeholder":"Email"}),
            "provincia":forms.Select(attrs={"class":"form-control b-r-xl","required":True}),
        }

    def __init__(self,*args,**kwargs):
        super(EntradaForm,self).__init__(*args,**kwargs)
        self.fields["provincia"].choices = Region.objects.none()

class EventoTransmitir(forms.Form):
    url = forms.URLInput(attrs={"class":"form-control b-r-xl","required":True})