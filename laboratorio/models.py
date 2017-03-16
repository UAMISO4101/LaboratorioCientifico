from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Rol(models.Model):
    nombre = models.CharField(max_length=100)

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=1000)
    imageFile = models.ImageField(upload_to='images', null=True,  blank=True)
    roles = models.ManyToManyField(Rol)

class TipoBodega(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

class Bodega(models.Model):
    serial = models.CharField(max_length=50, unique=True, null=True)
    nombre = models.CharField(max_length=100, null=True)
    ubicacion = models.CharField(max_length=100, null=True)
    niveles = models.IntegerField(null=True)
    secciones = models.IntegerField(null=True)
    temperatura_minima = models.DecimalField(null=True, max_digits=11,decimal_places=8)
    temperatura_media = models.DecimalField(null=True, max_digits=11,decimal_places=8)
    estado = models.BooleanField(default=True)
    usuario_creacion = models.IntegerField(null=True)
    usuario_actualizacion = models.IntegerField(null=True)
    fecha_creacion = models.DateTimeField(null=True)
    fecha_actualizacion = models.DateTimeField(null=True)
    tipo_bodega = models.ForeignKey(TipoBodega, null=True)
    usuario = models.ForeignKey(Usuario, null=True)