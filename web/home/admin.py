from django.contrib import admin
from home.models import *

# Register your models here.
# class AdminCliente(admin.ModelAdmin):
#     list_display = ('nombre', 'email', 'fecha', 'habilitado', 'premium', 'grupo')
#     list_filter = ('fecha', 'habilitado', 'premium','grupo')
#     ordering = ('-fecha',)
#     search_fields = ('email', 'nombre')
#
#     class Meta:
#         model = Cliente
#
#
# class AdminGrupo(admin.ModelAdmin):
#     pass
#
# admin.site.register(Cliente,AdminCliente)
# admin.site.register(Grupo,AdminGrupo)

admin.site.register(Contact)
admin.site.register(Motive)