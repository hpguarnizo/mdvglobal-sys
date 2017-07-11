from django import forms
from donacion.models import Pagina


class CantidadForm(forms.Form):
    cantidad = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control b-r-xl', 'min': '1',"required":True}))


class PaginaForm(forms.ModelForm):
    class Meta:
        model = Pagina
        fields = ['titulo','descripcion','imagen']
        widgets= {
            'titulo': forms.TextInput(attrs={'class':'form-control b-r-xl'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control b-r-xl'})
        }