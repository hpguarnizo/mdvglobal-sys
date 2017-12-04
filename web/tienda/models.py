import os
from datetime import datetime

from cities_light.models import City, Region
from django.contrib.sites.models import Site
from django.db import models

# Create your models here.
from model_utils.managers import InheritanceManager
from s3direct.fields import S3DirectField

from accounts.models import MyUser, _generate_code
from tienda.emails import email_envio


class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=256)

    def __str__(self):
        return self.nombre

    def get_nombre(self):
        return self.nombre

    def get_tipos(self):
        lista = []
        cant_total=0
        for tipo in TipoProducto.objects.all():
            cant_tipo=len(Producto.objects.filter(tipo=tipo,categoria=self,eliminado=False))
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

    def get_nombre(self):
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
    descuento = models.FloatField(null=True,blank=True)
    archivo = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    imagen = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    imagen2 = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    imagen3= S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'),null=True,blank=True)
    stock = models.IntegerField(null=True,blank=True)
    eliminado = models.BooleanField(default=False)
    cantidad_vendidos=models.IntegerField(default=0)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s-%s" %(self.nombre,self.tipo)

    def get_imagen2(self):
        return self.imagen2

    def get_nombre_corto(self):
        if len(self.nombre)>15:
            return self.nombre[:15]+"..."
        else:
            return self.nombre[:15]

    def get_imagen2_url(self):
        if self.imagen2:
            return self.imagen2
        else:
            return "/static/unify-ecommerce/img/blog/31.jpg"

    def get_imagen3_url(self):
        if self.imagen3:
            return self.imagen3
        else:
            return "/static/unify-ecommerce/img/blog/29.jpg"

    def get_imagen_url(self):
        if self.imagen:
            return self.imagen
        else:
            return "/static/unify-ecommerce/img/blog/25.jpg"

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

    def quitar_stock(self,cantidad):
        self.stock = self.stock-cantidad
        self.cantidad_vendidos+=cantidad
        self.save()

    def hay_stock_s(self):
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
        self.imagen2 = producto.imagen2
        self.imagen3 = producto.imagen3
        self.descuento = producto.descuento

    def eliminar(self):
        self.eliminado=True


    def get_descuento(self):
        return self.descuento

    def get_cantidad_vendidos(self):
        return self.cantidad_vendidos


    def get_precio_descuento(self):
        if self.descuento:
            if self.descuento>0 and self.descuento<100:
                return round(self.precio*(1-(self.descuento/100)),2)
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

    def enviar(self,compra,codigo,url):
        pass

    def __str__(self):
        return self.nombre


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
        if compra.tiene_libro_fisico():
            compra.set_estado(Pagado.objects.all().first())
            compra.quitar_stock()
        else:
            compra.set_estado(Enviado.objects.all().first())
        compra.save()

    def envio(self,compra,codigo,url):
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

    def enviar(self,compra,codigo,url):
        compra.set_codigo(codigo)
        compra.set_url_envio(url)
        compra.set_estado(Enviado.objects.all().first())
        compra.save()


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

    def enviar(self,compra,codigo,url):
        compra.set_codigo(codigo)
        compra.set_url_envio(url)
        compra.save()


class Compra(models.Model):
    token = models.CharField(max_length=256)
    nombre = models.CharField(max_length=256,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    direccion = models.CharField(max_length=256,null=True,blank=True)
    provincia = models.ForeignKey(Region,null=True,blank=True)
    ciudad = models.ForeignKey(City,null=True,blank=True)
    user = models.ForeignKey(MyUser,null=True,blank=True)
    total = models.FloatField(null=True,blank=True)
    estado = models.ForeignKey(EstadoCompra,default=1)
    fecha=models.DateField(auto_now_add=True)
    codigo_seguimiento = models.CharField(max_length=256,null=True,blank=True)
    url_envio = models.URLField(null=True,blank=True)

    def get_user(self):
        return self.user

    def __str__(self):
        return "%i-%s"%(self.id,self.get_nombre())

    def enviar_email_envio(self,request):
        email_envio(request,self)

    def verificar_libros(self):
        for detalle in self.get_detalle():
            if not detalle.get_producto().hay_stock(detalle.get_cantidad()):
                detalle.delete()
                return False
        return True

    def get_url_envio(self):
        return self.url_envio

    def get_codigo(self):
        return self.codigo_seguimiento

    def set_codigo(self,codigo):
        self.codigo_seguimiento = codigo

    def set_url_envio(self,url):
        self.url_envio = url

    def get_nombre(self):
        if self.user:
            return self.user.get_full_name()
        else:
           return self.nombre
    
    def tiene_libro_fisico(self):
        for detalle in self.get_detalle():
            if detalle.get_producto().get_tipo().es_libro_fisico():
                return True
        return False

    def get_email(self):
        if self.user:
            return self.user.get_email()
        else:
            return self.email

    def get_provincia(self):
        if self.user:
            return self.user.get_provincia()
        else:
            return self.provincia

    def get_ciudad(self):
        return self.ciudad

    def get_direccion(self):
        return self.direccion

    def get_estado(self):
        return EstadoCompra.objects.get_subclass(id=self.estado.id)

    def get_detalle(self):
        return DetalleCompra.objects.filter(compra=self)

    def get_total(self):
        if self.get_estado().es_incompleta:
            total= 0
            for detalle in self.get_detalle():
                total = total + detalle.get_parcial()
            return total
        else:
            return self.total

    def set_token(self):
        self.token = str(_generate_code())
        self.token = self.token[2:len(self.token)-1]

    def set_user(self,user):
        self.user = user

    def set_direccion(self,direccion):
        self.direccion = direccion

    def get_token(self):
        return str(self.token)

    def agregar_producto(self,producto,cantidad):
        if DetalleCompra.objects.filter(compra=self,producto=producto):
            detalle = DetalleCompra.objects.get(compra=self,producto=producto)
            detalle.agregar()
        else:
            if producto.get_tipo().es_libro_fisico() and cantidad>0:
                detalle =DetalleCompra(producto=producto,precio=producto.get_precio(),compra=self,cantidad=cantidad)
            else:
                detalle =DetalleCompra(producto=producto,precio=producto.get_precio(),compra=self)

        detalle.save()
        self.save()

    def set_total(self,total):
        self.total = total

    def pagar(self):
        self.get_estado().pagar(self)

    def set_estado(self,estado):
        self.estado = estado

    def quitar_stock(self):
        for detalle in self.get_detalle():
            detalle.quitar_stock()

    def enviar(self,codigo,url):
        self.get_estado().enviar(self,codigo,url)

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
        return self.precio

    def get_producto(self):
        return self.producto

    def get_parcial(self):
        return self.producto.get_precio_descuento()*self.cantidad

    def agregar(self):
        if self.producto.get_tipo().es_libro_fisico():
            self.cantidad = self.cantidad +1

    def quitar(self):
        if self.cantidad>1:
            self.cantidad = self.cantidad-1

    def quitar_stock(self):
        if self.producto.get_tipo().es_libro_fisico():
            if self.producto.get_stock()-self.cantidad>=0:
                self.producto.quitar_stock(self.cantidad)
            return False
        return True