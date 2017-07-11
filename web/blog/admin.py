from django.contrib import admin

# Register your models here.
from blog.models import Subscriber


class AdminDefault(admin.ModelAdmin):
    pass

admin.site.register(Subscriber,AdminDefault)