import os

from django.db import models

# Create your models here.
from s3direct.fields import S3DirectField


class Donacion(models.Model):
    nombre = models.CharField(max_length=256)
    fecha = models.DateField(auto_now_add=True)
    monto = models.FloatField()

    def get_nombre(self):
        return self.nombre

    def get_fecha(self):
        return "%i/%i/%i" % (self.fecha.day,self.fecha.month,self.fecha.year)

    def get_monto(self):
        return self.monto


class Pagina(models.Model):
    titulo = models.CharField(max_length=256)
    imagen = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    descripcion = models.TextField()

    def get_titulo(self):
        return self.titulo

    def get_imagen(self):
        return self.imagen

    def get_descripcion(self):
        return self.descripcion

    def set_data(self,pagina):
        self.titulo = pagina.titulo
        self.imagen = pagina.imagen
        self.descripcion = pagina.descripcion
