from django.contrib import admin
# Register your models here.
from evento.models import Evento, Categoria, Entrada

admin.site.register(Evento)
admin.site.register(Categoria)
admin.site.register(Entrada)