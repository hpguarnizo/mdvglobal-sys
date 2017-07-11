from django import forms

from tienda.models import CategoriaProducto
from tienda.models import Producto


class NuevoProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','categoria','tipo','archivo','stock','imagen']
        widgets ={
            'nombre':forms.TextInput(attrs={'class':'form-control b-r-xl','maxlength':'256','required':True}),
            'descripcion': forms.Textarea(attrs={'class':'form-control b-r-xl','required':True}),
            'precio': forms.NumberInput(attrs={'class':'form-control b-r-xl',"min":"1",'required':True}),
            'stock': forms.NumberInput(attrs={'class':'form-control b-r-xl',"min":"1"}),
            'categoria': forms.Select(attrs={'class':'form-control b-r-xl','required':True}),
            'tipo': forms.Select(attrs={'class':'form-control b-r-xl','required':True}),
        }

class EditarProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','categoria','stock','imagen']
        widgets ={
            'nombre':forms.TextInput(attrs={'class':'form-control b-r-xl','maxlength':'256','required':True}),
            'descripcion': forms.Textarea(attrs={'class':'form-control b-r-xl','required':True}),
            'precio': forms.NumberInput(attrs={'class':'form-control b-r-xl',"min":"1",'required':True}),
            'stock': forms.NumberInput(attrs={'class':'form-control b-r-xl',"min":"1"}),
            'categoria': forms.Select(attrs={'class':'form-control b-r-xl','required':True}),
        }


class NuevaCategoria(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields= ["nombre"]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control b-r-xl','maxlength':'256' ,'required':True})
        }