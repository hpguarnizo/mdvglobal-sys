import os
from django.db import models
from s3direct.fields import S3DirectField
from pay.models import Plan



class CategoriaContenido(models.Model):
    nombre = models.CharField(max_length=256)

    def __str__(self):
        return self.nombre

    def get_nombre(self):
        return self.nombre

    def get_tipos(self):
        lista = []
        cant_total = 0
        for tipo in TipoContenido.objects.all():
            cant_tipo = len(Contenido.objects.filter(tipo=tipo, categoria=self))
            cant_total += cant_tipo
            lista.append(cant_tipo)
        lista.append(cant_total)
        return lista

    def set_nombre(self,nombre):
        self.nombre= nombre

    def get_cantidad(self):
        return len(Contenido.objects.filter(categoria=self))


class TipoContenido(models.Model):
    nombre = models.CharField(max_length=256)

    def __str__(self):
        return self.nombre

    def get_nombre(self):
        return self.nombre

    def es_audio(self):
        return (self.nombre=="Audio")

    def es_video(self):
        return (self.nombre=="Video")

    def es_documento(self):
        return (self.nombre=="Documento")

    def get_cantidad(self):
        return len(Contenido.objects.filter(tipo=self))


class Contenido(models.Model):
    nombre = models.CharField(max_length=256)
    descripcion = models.TextField()
    imagen = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    categoria = models.ForeignKey(CategoriaContenido)
    tipo = models.ForeignKey(TipoContenido)
    archivo = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    acceso = models.ForeignKey(Plan)
    fecha = models.DateField(auto_now_add=True)

    def get_nombre(self):
        return self.nombre

    def get_descripcion(self):
        return self.descripcion

    def get_imagen(self):
        if self.imagen:
            return self.imagen
        else:
            return '/static/unify/img/team/img1-md.jpg'

    def get_categoria(self):
        return self.categoria

    def get_tipo(self):
        return self.tipo

    def get_archivo(self):
        return self.archivo

    def get_acceso(self):
        return Plan.objects.get_subclass(id=self.acceso.id)

    def set_data(self,contenido):
        self.nombre= contenido.nombre
        self.descripcion = contenido.descripcion
        self.imagen = contenido.imagen
        self.categoria = contenido.categoria
        self.tipo = contenido.tipo
        self.archivo = contenido.archivo
        self.acceso = contenido.acceso

    def puede_verlo(self,user):
        if user.get_plan().es_ministerial():
            return True
        if user.get_plan().es_premium() and not self.get_acceso().es_ministerial():
            return True
        if user.get_plan().es_gratis and not self.get_acceso().es_ministerial() and not self.get_acceso().es_premium():
            return True
        return False