from django.contrib import admin
from pay.models import Customer,Gratis,Premium, Ministerial

# Register your models here.

admin.site.register(Customer)
admin.site.register(Gratis)
admin.site.register(Premium)
admin.site.register(Ministerial)
