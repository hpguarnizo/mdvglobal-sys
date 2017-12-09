from cities_light.models import City
from django import forms
from tienda.models import CategoriaProducto, Compra
from tienda.models import Producto


class NuevoProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre',"descuento",'descripcion','precio','categoria','tipo','archivo','stock','imagen','imagen2','imagen3']
        widgets ={
            'nombre':forms.TextInput(attrs={'class':'form-control b-r-xl','maxlength':'256','required':True}),
            'descripcion': forms.Textarea(attrs={'class':'form-control b-r-xl','required':True}),
            'precio': forms.NumberInput(attrs={'class':'form-control b-r-xl',"min":"1",'required':True}),
            'descuento': forms.NumberInput(attrs={'class':'form-control b-r-xl',"min":"1","max":99}),
            'stock': forms.NumberInput(attrs={'class':'form-control b-r-xl',"min":"1"}),
            'categoria': forms.Select(attrs={'class':'form-control b-r-xl','required':True}),
            'tipo': forms.Select(attrs={'class':'form-control b-r-xl','required':True}),
        }

class EditarProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','categoria','stock','imagen',"descuento",'imagen2','imagen3','archivo']
        widgets ={
            'nombre':forms.TextInput(attrs={'class':'form-control b-r-xl','maxlength':'256','required':True}),
            'descripcion': forms.Textarea(attrs={'class':'form-control b-r-xl','required':True}),
            'precio': forms.NumberInput(attrs={'class':'form-control b-r-xl',"min":"1",'required':True}),
            'stock': forms.NumberInput(attrs={'class':'form-control b-r-xl',"min":"1"}),
            'categoria': forms.Select(attrs={'class':'form-control b-r-xl','required':True}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control b-r-xl', "min": "1", "max": 99}),

        }


class NuevaCategoria(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields= ["nombre"]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control b-r-xl','maxlength':'256' ,'required':True})
        }

class CompraForm(forms.ModelForm):
    class Meta:
        model=Compra
        fields=["nombre","direccion","email","provincia","ciudad"]
        widgets={
            'nombre': forms.TextInput(attrs={'class': 'form-control b-r-xl', 'maxlength': '256', 'required': True,"placeholder":"Nombre"}),
            'direccion': forms.TextInput(attrs={'class': 'form-control b-r-xl', 'maxlength': '256', 'required': True,"placeholder":"Direccion"}),
            'email': forms.EmailInput(attrs={'class': 'form-control b-r-xl', 'maxlength': '256',"placeholder":"Email"}),
            'provincia': forms.Select(attrs={'class': 'form-control b-r-xl', 'required': True}),
            'ciudad': forms.Select(attrs={'class': 'form-control b-r-xl', 'required': True}),

        }

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        self.fields["ciudad"].choices = City.objects.none()


class CompletarCompra(forms.ModelForm):
    class Meta:
        model=Compra
        fields=["direccion","email","provincia","ciudad"]
        widgets={
            'direccion': forms.TextInput(attrs={'class': 'form-control b-r-xl', 'maxlength': '256',
                                                'required': True,"placeholder":"Direccion"}),
            'email': forms.EmailInput(attrs={'class': 'form-control b-r-xl', 'maxlength': '256',"placeholder":"Email"}),
            'provincia': forms.Select(attrs={'class': 'form-control b-r-xl', 'required': True}),
            'ciudad': forms.Select(attrs={'class': 'form-control b-r-xl', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super(CompletarCompra, self).__init__(*args, **kwargs)
        self.fields["ciudad"].choices = City.objects.none()


class EnviarCompraForm(forms.Form):
    codigo=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control b-r-xl', 'maxlength': '256',
                                                         'required': True,"placeholder":"Codigo..."}))
    url=forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control b-r-xl', 'maxlength': '256',
                                                    'required': True,"placeholder":"https://www.oca.com"}))