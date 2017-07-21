import os
from datetime import datetime

from cities_light.models import City, Region
from django.db import models

# Create your models here.
from model_utils.managers import InheritanceManager
from s3direct.fields import S3DirectField

from accounts.models import MyUser, _generate_code


class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=256)

    def __str__(self):
        return self.nombre

    def get_tipos(self):
        lista = []
        cant_total=0
        for tipo in TipoProducto.objects.all():
            cant_tipo=len(Producto.objects.filter(tipo=tipo,categoria=self))
            cant_total+= cant_tipo
            lista.append(cant_tipo)
        lista.append(cant_total)
        return lista

    def set_nombre(self,nombre):
        self.nombre = nombre

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre

    def mas_vendidos(self):
        return Producto.objects.filter(tipo=self.id).order_by('cantidad_vendidos')[:3]

    def es_libro_fisico(self):
        return (self.id==4)

class Producto(models.Model):
    nombre = models.CharField(max_length=256)
    descripcion = models.TextField()
    precio = models.FloatField()
    categoria = models.ForeignKey(CategoriaProducto)
    tipo = models.ForeignKey(TipoProducto)
    descuento = models.FloatField()
    archivo = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    imagen = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    imagen2 = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    imagen3= S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    stock = models.IntegerField(null=True,blank=True)
    eliminado = models.BooleanField(default=False)
    cantidad_vendidos=models.IntegerField(default=0)
    fecha = models.DateField(auto_now_add=True)

    def get_imagen2(self):
        return self.imagen2

    def get_imagen3(self):
        return self.imagen3

    def get_nombre(self):
        return self.nombre

    def get_descripcion(self):
        return self.descripcion

    def get_precio(self):
        return self.precio

    def get_categoria(self):
        return self.categoria

    def get_tipo(self):
        return self.tipo

    def get_archivo(self):
        return self.archivo

    def get_imagen(self):
        return self.imagen

    def get_stock(self):
        return self.stock

    def hay_stock(self):
        if self.tipo.es_libro_fisico and self.stock==0:
            return False
        else:
            return True

    def hay_stock(self,cantidad):
        if self.tipo.es_libro_fisico() and (self.stock-cantidad)<0:
            return False
        else:
            return True

    def subido_este_mes(self):
        now = datetime.now()
        return (now.year==self.fecha.year and now.month==self.fecha.month)

    def set_data(self,producto):
        self.stock = producto.stock
        self.nombre= producto.nombre
        self.descripcion= producto.descripcion
        self.precio = producto.precio
        self.categoria= producto.categoria
        self.imagen = producto.imagen

    def eliminar(self):
        self.eliminado=True


    def get_descuento(self):
        self.descuento


    def get_precio_descuento(self):
        if self.descuento>0:
            return self.precio*100/self.descuento
        else:
            return self.precio


class EstadoCompra(models.Model):
    nombre = models.CharField(max_length=25)
    objects = InheritanceManager()

    def es_incompleta(self):
        return False

    def es_pagado(self):
        return False

    def es_enviado(self):
        return False

    def enviar(self,compra):
        pass

    def pagar(self,compra):
        pass


class Incompleta(EstadoCompra):
    def es_incompleta(self):
        return True

    def es_pagado(self):
        return False

    def es_enviado(self):
        return False

    def enviar(self,compra):
        pass

    def pagar(self,compra):
        pass


class Pagado(EstadoCompra):
    def es_pagado(self):
        return True

    def es_incompleta(self):
        return False

    def es_enviado(self):
        return False

    def enviar(self,compra):
        pass

    def pagar(self,compra):
        pass


class Enviado(EstadoCompra):
    def es_enviado(self):
        return True

    def es_pagado(self):
        return False

    def es_incompleta(self):
        return False

    def enviar(self,compra):
        pass

    def pagar(self,compra):
        pass



class Compra(models.Model):
    token = models.CharField(max_length=256)
    nombre = models.CharField(max_length=256,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    direccion = models.CharField(max_length=256,null=True,blank=True)
    provincia = models.ForeignKey(Region,null=True,blank=True)
    ciudad = models.ForeignKey(City,null=True,blank=True)
    user = models.ForeignKey(MyUser,null=True,blank=True)
    total = models.FloatField(default=0)
    estado = models.ForeignKey(EstadoCompra,default=1)


    def get_estado(self):
        return EstadoCompra.objects.get_subclass(id=self.estado.id)

    def get_detalle(self):
        return DetalleCompra.objects.filter(compra=self)

    def get_total(self):
        return self.total

    def set_token(self):
        self.token = _generate_code()

    def agregar_producto(self,producto,cantidad):
        if DetalleCompra.objects.filter(compra=self,producto=producto):
            detalle = DetalleCompra.objects.get(compra=self,producto=producto)
            self.total = self.total + producto.get_precio()
            detalle.agregar()
        else:
            if producto.get_tipo().es_libro_fisico() and cantidad>0:
                detalle =DetalleCompra(producto=producto,precio=producto.get_precio(),compra=self,cantidad=cantidad)
                self.total = self.total + producto.get_precio() * cantidad
            else:
                detalle =DetalleCompra(producto=producto,precio=producto.get_precio(),compra=self)
                self.total = self.total + producto.get_precio()

        detalle.save()
        self.save()


class DetalleCompra(models.Model):
    producto = models.ForeignKey(Producto)
    precio = models.FloatField()
    cantidad = models.IntegerField(default=1)
    compra = models.ForeignKey(Compra)

    def get_compra(self):
        return self.compra

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.cantidad

    def get_producto(self):
        return self.producto

    def get_parcial(self):
        return self.producto.get_precio()*self.cantidad

    def agregar(self):
        self.cantidad = self.cantidad +1