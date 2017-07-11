from django.contrib import admin

# Register your models here.
from donacion.models import Pagina, Donacion

admin.site.register(Donacion)
admin.site.register(Pagina)
