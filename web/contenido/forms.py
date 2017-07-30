from django import forms

from contenido.models import Contenido, CategoriaContenido


class NuevoContenidoForm(forms.ModelForm):
    class Meta:
        model=Contenido
        fields=['nombre','descripcion','imagen','categoria','tipo','archivo','acceso']
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control b-r-xl','maxlength':'256','required':True}),
            'descripcion':forms.Textarea(attrs={'class':'form-control b-r-xl','required':True}),
            'categoria':forms.Select(attrs={'class':'form-control b-r-xl','required':True}),
            'tipo':forms.Select(attrs={'class':'form-control b-r-xl','required':True}),
            'acceso':forms.Select(attrs={'class':'form-control b-r-xl','required':True}),
        }


class NuevaCategoria(forms.ModelForm):
    class Meta:
        model = CategoriaContenido
        fields= ["nombre"]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control b-r-xl','maxlength':'256' ,'required':True})
        }