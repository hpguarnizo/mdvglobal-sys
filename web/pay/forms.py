from django import forms

class PlanesConfigForm(forms.Form):
    gratis = forms.FloatField(widget=forms.NumberInput(attrs={"class":"form-control b-r-xl","required":False}))
    premium = forms.FloatField(widget=forms.NumberInput(attrs={"class":"form-control b-r-xl","required":False}))
    ministerial = forms.FloatField(widget=forms.NumberInput(attrs={"class":"form-control b-r-xl","required":False}))