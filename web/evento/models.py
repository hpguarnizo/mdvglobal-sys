import os
import random

import datetime
from django.contrib.sites.models import Site
from django.urls import reverse
from django.utils.functional import SimpleLazyObject
from django.utils.timezone import now
from cities_light.models import Region, City
from django.db import models
from s3direct.fields import S3DirectField
from model_utils.managers import InheritanceManager
from accounts.models import MyUser


class TipoEvento(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

    def es_pago(self):
        return (self.nombre=="Pago")

class Categoria(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

    def es_presencial(self):
        return (self.nombre=="Presencial")

class EstadoEvento(models.Model):
    nombre = models.CharField(max_length=20)
    objects = InheritanceManager()
    def __str__(self):
        return self.nombre

    def es_disponible(self):
        return False

    def es_lleno(self):
        return False

    def es_terminado(self):
        return False

    def es_en_vivo(self):
        return False

    def transmitir(self,evento):
        pass

    def finalizar_transmision(self,estado):
        pass

class Disponible(EstadoEvento):

    def es_disponible(self):
        return True

    def es_lleno(self):
        return False

    def es_terminado(self):
        return False

    def se_lleno(self,evento):
        if evento.get_asistentes()>=evento.get_cupo() and evento.get_categoria().es_presencial():
            evento.set_estado(Lleno.objects.all().first())
            evento.save()

    def terminar(self,evento):
        evento.set_estado(Terminado.objects.all().first())

    def set_cupo(self,evento,cupo):
        if cupo > evento.get_asistentes():
            evento.set_cupo(cupo)
        elif cupo== evento.get_asistentes():
            evento.set_cupo(cupo)
            evento.set_estado(Lleno.objects.all().first())

    def es_en_vivo(self):
        return False

    def transmitir(self,evento):
        evento.set_estado(EnVivo.objects.all().first())
        evento.save()

    def finalizar_transmision(self,estado):
        pass

class Lleno(EstadoEvento):

    def es_lleno(self):
        return True

    def es_disponible(self):
        return False

    def es_terminado(self):
        return False

    def se_lleno(self,evento):
        pass

    def terminar(self,evento):
        evento.set_estado(Terminado.objects.all().first())

    def set_cupo(self,evento,cupo):
        if cupo > evento.get_cupo():
            evento.set_cupo(cupo)
            evento.set_estado(Disponible.objects.all().first())

    def es_en_vivo(self):
        return False

    def transmitir(self,evento):
        evento.set_estado(EnVivo.objects.all().first())
        evento.save()

    def finalizar_transmision(self,evento):
        pass

class Terminado(EstadoEvento):

    def es_disponible(self):
        return False

    def es_lleno(self):
        return False

    def es_terminado(self):
        return True

    def se_lleno(self):
        pass

    def se_lleno(self, evento):
        pass

    def terminar(self,evento):
        pass

    def set_cupo(self,evento,cupo):
        pass

    def es_en_vivo(self):
        return False

    def transmitir(self,evento):
        pass

    def finalizar_transmision(self,evento):
        pass


class EnVivo(EstadoEvento):

    def es_disponible(self):
        return False

    def es_lleno(self):
        return False

    def es_terminado(self):
        return False

    def es_en_vivo(self):
        return True

    def se_lleno(self):
        pass

    def se_lleno(self, evento):
        pass

    def terminar(self,evento):
        pass

    def set_cupo(self,evento,cupo):
        pass

    def transmitir(self,evento):
        pass

    def finalizar_transmision(self,evento):
        evento.set_estado(Terminado.objects.all().first())
        evento.save()


# Create your models here.
class Evento(models.Model):
    nombre = models.CharField(max_length=256)
    descripcion = models.TextField()
    imagen = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    fecha = models.DateField()
    cupo = models.PositiveIntegerField(blank=True,null=True)
    asistentes = models.PositiveIntegerField(default=0)
    precio = models.FloatField(blank=True,null=True)
    categoria = models.ForeignKey(Categoria)
    direccion = models.CharField(max_length=256,blank=True,null=True)
    provincia = models.ForeignKey(Region,blank=True,null=True)
    ciudad = models.ForeignKey(City,blank=True,null=True)
    tipo_evento = models.ForeignKey(TipoEvento)
    estado = models.ForeignKey(EstadoEvento,default=1)
    url = models.TextField(null=True,blank=True)

    def finalizar_transmision(self):
        self.get_estado().finalizar_transmision(self)

    def transmitir(self,url):
        self.url = url
        self.get_estado().transmitir(self)

    def __str__(self):
        return self.nombre

    def get_imagen_url(self):
        if self.imagen:
            return self.imagen
        else:
            return "/static/unify-ecommerce/img/blog/14.jpg"

    def get_cupo(self):
        return self.cupo

    def get_fecha(self):
        return "%i/%i/%i" % (self.fecha.day,self.fecha.month,self.fecha.year)

    def get_asistentes(self):
        return self.asistentes

    def set_estado(self,estado):
        self.estado = estado

    def get_entradas(self):
        return Entrada.objects.filter(evento=self.id)

    def get_categoria(self):
        return self.categoria

    def get_nombre(self):
        return self.nombre

    def get_cupo(self):
        return self.cupo

    def get_precio(self):
        return self.precio

    def get_direccion(self):
        return self.direccion

    def get_ciudad(self):
        return self.ciudad

    def get_tipo(self):
        return self.tipo_evento

    def get_descripcion(self):
        return self.descripcion

    def get_estado(self):
        return EstadoEvento.objects.get_subclass(id=self.estado.id)

    def es_precio_valido(self):
        if self.tipo_evento.id==1 and self.precio>0:
            return True
        elif self.tipo_evento.id==2:
            return True
        else:
            return False

    def es_fecha_valida(self):
        if self.fecha<now().date():
            return False
        else:
            return True

    def set_data(self,nombre,descripcion,cupo,precio,direccion,imagen,fecha):
        self.nombre = nombre
        self.descripcion = descripcion
        self.get_estado().set_cupo(self,cupo)
        self.fecha=fecha

        aux_precio = self.precio
        self.precio = precio
        if not self.es_precio_valido():
            self.precio = aux_precio

        self.direccion = direccion
        self.imagen = imagen

    def set_cupo(self,cupo):
        self.cupo = cupo

    def get_transmision(self):
        return self.url

    def get_url(self):
        return Site.objects.get_current().domain + reverse('evento_seleccionar',kwargs={'evento_id':self.id})

    def es_nuevo(self):
        if (datetime.datetime.now().date() - self.fecha) < datetime.timedelta(days=8):
            return True
        else:
            return False

class EstadoEntrada(models.Model):
    nombre = models.CharField(max_length=20)
    objects = InheritanceManager()

    def __str__(self):
        return self.nombre

    def pagar(self,entrada):
        pass

    def es_sin_pagar(self):
        return False

    def es_pagada(self):
        return False

    def es_validada(self):
        return False

    def asistir(self,entrada):
        pass

class SinPagar(EstadoEntrada):

    def pagar(self,entrada):
        entrada.set_estado(Pagada.objects.all().first())
        entrada.save()

    def es_sin_pagar(self):
        return True

    def es_pagada(self):
        return False

    def es_validada(self):
        return False

    def asistir(self, entrada):
        pass

class Pagada(EstadoEntrada):
    def pagar(self, entrada):
        pass

    def es_pagada(self):
        return True

    def es_sin_pagar(self):
        return False

    def es_validada(self):
        return False

    def asistir(self, entrada):
        entrada.set_Estado(Validada.objects.all().first())
        entrada.save()

class Validada(EstadoEntrada):
    def pagar(self, entrada):
        pass

    def es_validada(self):
        return True

    def es_pagada(self):
        return False

    def es_sin_pagar(self):
        return False

    def asistir(self, entrada):
        pass

class Entrada(models.Model):
    user = models.ForeignKey(MyUser,null=True,blank=True)
    codigo = models.CharField(max_length=256 ,null=True,blank=True)
    nombre = models.CharField(max_length=256 ,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    provincia = models.ForeignKey(Region,null=True,blank=True)
    estado = models.ForeignKey(EstadoEntrada,null=True,blank=True,default=1)
    evento = models.ForeignKey(Evento,null=True,blank=True)

    def __str__(self):
        return self.estado

    def set_codigo(self):
        self.codigo = hex((self.id * 2) + random.randrange(start=1, stop=100) + 1439)[2:]

    def get_user(self):
        return self.user

    def get_codigo(self):
        return self.codigo

    def get_nombre(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return self.nombre

    def get_email(self):
        if self.user:
            return self.user.get_email()
        else:
            return self.email

    def get_provincia(self):
        if self.user:
            return self.user.get_provincia
        else:
            return self.provincia

    def get_estado(self):
        return EstadoEntrada.objects.get_subclass(id=self.estado.id)

    def get_evento(self):
        return self.evento

    def set_estado(self,estado):
        self.estado=estado

    def set_evento(self,evento):
        self.evento = evento

    def pagar(self,entrada):
        self.get_estado().pagar(entrada)

    def asistir(self):
        self.get_estado().asistir(self)