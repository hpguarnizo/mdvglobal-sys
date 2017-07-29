from django.contrib import admin
# Register your models here.
from evento.models import Evento, Categoria, Entrada, EstadoEntrada

admin.site.register(Evento)
admin.site.register(Categoria)
admin.site.register(Entrada)
admin.site.register(EstadoEntrada)